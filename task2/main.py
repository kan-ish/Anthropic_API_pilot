from anthropic import Anthropic
from dotenv import load_dotenv
import os
import re
from datetime import datetime
import sqlite3
import json

load_dotenv()

CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')

client = Anthropic(api_key=CLAUDE_API_KEY)
MODEL_NAME = "claude-3-5-sonnet-20240620"
db_path = os.path.join(".", "blogs.db")

# user_message = input("Ask me anything: ")

tools = [
        {
            "name": "save_blog",
            "description": """The content of the blog article to be saved to database. 
            If more information is required from the user, enclose required information in <expecting_input> tags and comma-separate them
            Eg - <expecting_input>author,title</expecting_input>. Do NOT infer any values.""",
            "input_schema": {
                "type": "object",
                "properties": {
                    "body": {
                        "type": "string",
                        "description": "Body of the blog enclosed in <article></article> tags. Do not include the tags in the body." 
                    },
                    "title": {
                        "type": "string",
                        "description": "Title of the article." 
                    },
                    "author": {
                        "type": "string",
                        "description": "Name of the author of the article." 
                    },
                    "id": {
                        "type": "string",
                        "description": "Unique id of the article in the database. Only needed when updating an existing article." 
                    }
                },
                "required": ["author", "title", "body"]
            }
        },
        {
            "name": "retrieve_blog",
            "description": "The content of a blog article to be retrieved from database.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Title of the article." 
                    },
                    "author": {
                        "type": "string",
                        "description": "Name of the author of the article." 
                    },
                },
                "required": ["author", "title"]
            }
        },
        {
            "name": "delete_existing_blog",
            "description": "A blog article to be deleted from database.",
            "input_schema": {
                "type": "object",
                "properties": {}
            }
        }
    ]

system_message = """
Your only job is to generate, save, retrieve, update, and delete blog articles. 
You may generate blogs by responding to users' requests without using any tools.
To save, retrieve, update, and delete, you have access to the following tools - ['save_blog', 'retrieve_blog', 'delete_existing_blog']. 
The user may ask to generate a new blog article given some information, modify the blog in the conversation, or the user may ask to retrieve an existing article from the db. 
If the user has NOT EXPLICITLY asked to save, update, discard or delete the article, do NOT use those tools.
Do NOT infer any values. If you require any clarification, ask the user. Eg - 
<expecting_input>
    author,title
</expecting_input>.
When generating a blog article, Enclose the article as such:
<article>
    $article
</article>
"""

def save_blog(tool_input):
    if not tool_input["author"]:
        return "Error: Author not provided"
    if not tool_input["title"]:
        return "Error: Title not provided"
    if not tool_input["body"]:
        return "Error: Article body not provided"
    
    author = tool_input["author"]
    title = tool_input["title"]
    body = tool_input["body"]
    time_now = datetime.today().strftime('%Y-%m-%d %H:%M')
    id = tool_input.get("id", None)
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        if id is not None:
            cursor.execute("""
                UPDATE articles
                SET title = ?, author = ?, body = ?, date_published = ?
                WHERE id = ?
            """, (title, author, body, time_now, id))
        else:
            cursor.execute("""
                INSERT INTO articles (title, author, body, date_published)
                VALUES (?, ?, ?, ?)
            """, (title, author, body, time_now))

        conn.commit()
        print("Data inserted successfully")
        return "Data inserted successfully"
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return f"An error occurred: {e}"
    finally:
        if conn:
            conn.close()


def retrieve_blog(tool_input):
    if not tool_input["author"]:
        return "Error: Author not provided"
    if not tool_input["title"]:
        return "Error: Title not provided"

    author = tool_input["author"]
    title = tool_input["title"]

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM articles WHERE title = ?
            AND author = ?
        """, (title, author))

        rows = cursor.fetchall()
        if not rows:
            return "Error: No article found"
        
        print(f"Data from db: {rows}")
        result = {
            "id": rows[0][0],
            "title": rows[0][1],
            "author": rows[0][2],
            "body": rows[0][3],
            "date_published": rows[0][4],
        }
        print(f"\nformatted result: {result}")
        print(json.dumps(result))

        return json.dumps(result)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return f"An error occurred: {e}"
    finally:
        if conn:
            conn.close()

def conversate(system_message, input_query = "Ask me anything: ", response = None):
    if response:
        assistan_response = next(
            (block.text for block in response.content if hasattr(block, "text")),
            None,
        )
        print(f"\nAssistent response: {assistan_response}")
    # print("****SYSTEM MESSAGE*****")
    # print(system_message)
    # print("*********")
    
    user_message = input(input_query)

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=1024,
        tools=tools,
        messages=[{
            "role": "user",
            "content": user_message
        }],
        system=system_message
    )
    print(response)

    if response.stop_reason == "tool_use":
        tool_use = next(block for block in response.content if block.type == "tool_use")
        tool_name = tool_use.name
        tool_input = tool_use.input
        
        result = ""
        if tool_name == "save_blog":
            print("Saving the blog.")
            print(next(block.text for block in response.content if block.type == "text"))
            result = save_blog(tool_input)
        elif tool_name == "retrieve_blog":
            print("Retrieving the blog.")
            print(next(block.text for block in response.content if block.type == "text"))
            result = retrieve_blog(tool_input)

        print(f"\nTool Used: {tool_name}")
        print(f"Tool Input: {tool_input}")

        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=4096,
            messages=[
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": response.content},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_use.id,
                            "content": result,
                        }
                    ],
                },
            ],
            tools=tools,
        )
        return response
    else:
        modified_system_message = system_message + response.content[0].text
        
        if "</expecting_input>" in response.content[0].text:
            required_info = re.search(r'<expecting_input>(.*?)</expecting_input>', response.content[0].text, re.DOTALL).group(1)
            input_query = f"Please provide the following information required to save your blog - {required_info}: "
            return conversate(modified_system_message, input_query)
        else:
            return conversate(modified_system_message)


response = conversate(system_message) # Initiate conversation
print(response)
final_response = next(
    (block.text for block in response.content if hasattr(block, "text")),
    None,
)
print(f"\nFinal Response: {final_response}")

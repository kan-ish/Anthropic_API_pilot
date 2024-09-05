from anthropic import Anthropic
from dotenv import load_dotenv
import os
from tools_config import tools
from custom_functions import save_blog, retrieve_blog, delete_existing_blog, continue_conversation

load_dotenv()

CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
client = Anthropic(api_key=CLAUDE_API_KEY)
MODEL_NAME = "claude-3-5-sonnet-20240620"
db_path = os.path.join(".", "blogs.db")

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


def conversate(system_message, input_query = "Ask me anything: ", response = None):
    if response:
        assistan_response = next(
            (block.text for block in response.content if hasattr(block, "text")),
            None,
        )
        print(f"\nAssistant response: {assistan_response}")
    
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
    # print(response)

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
        elif tool_name == "delete_existing_blog":
            print("Deleting the blog.")
            print(next(block.text for block in response.content if block.type == "text"))
            result = delete_existing_blog(tool_input)

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

    continue_conversation(system_message, response, conversate)


response = conversate(system_message) # Initiate conversation

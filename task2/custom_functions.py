from datetime import datetime
import sqlite3
import json
import os
import re

db_path = os.path.join(".", "blogs.db")


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


def delete_existing_blog(tool_input):
    if not tool_input["id"]:
        return "Error: Please provide the unique id of the article. You can ask Claude to retrieve the id of the article you want to delete."
    
    id = tool_input["id"]

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM articles
            WHERE id = ?
        """, (id,))
        conn.commit()
        
        rows_affected = cursor.rowcount
        print(f"Deleted {rows_affected} records from db.")
        return f"Deleted {rows_affected} records from db."
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return f"An error occurred: {e}"
    finally:
        if conn:
            conn.close()


def extract_required_info(text):
    match = re.search(r'<expecting_input>(.*?)</expecting_input>', text, re.DOTALL)
    return match.group(1) if match else None


def continue_conversation(system_message, response, conversate):
    response_text = response.content[0].text
    modified_system_message = system_message + response_text
    
    required_info = extract_required_info(response_text)
    if required_info:
        input_query = f"Please provide the following information required to save your blog - {required_info}: "
        return conversate(modified_system_message, input_query, response)
    
    return conversate(modified_system_message, response=response)
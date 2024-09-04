from anthropic import Anthropic
from dotenv import load_dotenv
import os
import requests

load_dotenv()

CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')

client = Anthropic(api_key=CLAUDE_API_KEY)
MODEL_NAME = "claude-3-opus-20240229"

# user_message = input("Ask me anything: ")

tools = [
        {
            "name": "save_blog",
            "description": "The content of the blog article to be saved to database.",
            "input_schema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "retrieve_blog",
            "description": "The content of a blog article to be retrieved from database.",
            "input_schema": {
                "type": "object",
                "properties": {}
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
You may generate blogs by responding to users' requests normally.
To save, retrieve, update, and delete, you have access to the following tools - ['save_blog', 'retrieve_blog', 'delete_existing_blog']. 
The user may ask to generate a new blog article given some information, or the user may ask to retrieve an existing article. 
Until the user has EXPLICITLY asked to save, update, discard or delete the article, respond to the user's request normally.
When generating a blog article, Enclose the article as such:
<article>
    $article
</article>
"""

# def generate_or_modify_blog():
#     user_message = input("Further instructions: ")

#     return user_message

# def get_location():
#     """Takes the name of a city as input from user and then gets the lat and long of the city, then uses these to get the weater forecast from the public open-meteo API."""

#     city = input("Your current location (city): ")

#     url = "https://nominatim.openstreetmap.org/search"
#     params = {'q': city, 'format': 'json', 'limit': 1}
#     response = requests.get(url, params=params).json()
    
#     if response:
#         lat = response[0]["lat"]
#         lon = response[0]["lon"]
#         return {"lattitude": lat, "longitude": lon}
#     else:
#         raise ValueError("Could not find lat and long coordinates for given place.")

# response = client.messages.create(
#     model=MODEL_NAME,
#     max_tokens=1024,
#     tools=tools,
#     messages=[{
#         "role": "user",
#         "content": user_message
#     }],
#     system=system_message
# )
# print(response)

def conversate(system_message):
    user_message = input("Ask me anything: ")

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

        if tool_name == "save_blog":
            print("Save the blog.")
            print(next(block.text for block in response.content if block.type == "text"))

        print(f"\nTool Used: {tool_name}")
        print(f"Tool Input: {tool_input}")

        # further_instructions = generate_or_modify_blog()

        # response = client.messages.create(
        #     model=MODEL_NAME,
        #     max_tokens=4096,
        #     messages=[
        #         {"role": "user", "content": user_message},
        #         {"role": "assistant", "content": response.content},
        #         {
        #             "role": "user",
        #             "content": [
        #                 {
        #                     "type": "tool_result",
        #                     "tool_use_id": tool_use.id,
        #                     "content": further_instructions,
        #                 }
        #             ],
        #         },
        #     ],
        #     tools=tools,
        # )
    else:
        modified_system_message = system_message + response.content[0].text
        conversate(modified_system_message)


conversate(system_message)

# final_response = next(
#     (block.text for block in response.content if hasattr(block, "text")),
#     None,
# )
# print(response.content)
# print(f"\nFinal Response: {final_response}")

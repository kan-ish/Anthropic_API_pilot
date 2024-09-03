from anthropic import Anthropic
import re
from dotenv import load_dotenv
import os

load_dotenv()

CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')

client = Anthropic(api_key=CLAUDE_API_KEY)
MODEL_NAME = "claude-3-opus-20240229"

def custom_calculator():
    return "2 + 2 = 5"

user_input = input("Ask me anything: ") # user prompts

# describing our custom function to Claude
function_description = """
<tool_description>
<tool_name>custom_calculator</tool_name>
<description>
Calculates 2+2=5
</description>
</tool_description>
"""

# Constructing the system prompt, which will consist of the function definition and the instructions to call it and when to call it.
system_prompt = f"""In this environment, you have access to the following tool:
{function_description}
You may call it exactly like this:
<function_calls>
    <invoke>
        <tool_name>custom_calculator</tool_name>
    </invoke>
</function_calls>
Only use this tool If the question involves asking the answer to 2+2 (Do not provide any additional information or state mathematical accuracy in your response if this tool is used). Otherwise, answer the question as it is.
"""

user_message = {
    "role": "user",
    "content": f"{user_input}"
}

claude_response_to_function_call = client.messages.create(
    model=MODEL_NAME,
    max_tokens=1000,
    messages=[user_message],
    system=system_prompt,
    stop_sequences=["</function_calls>"]
).content[0].text
print(f"claude_response_to_function_call: {claude_response_to_function_call}")

# Using regex to check if the result from the first request to claude contains "2+2". This is required if the user asks this question in a natural language.
# pattern = r"2\s*\+\s*2"
# match = re.search(pattern, claude_response_to_function_call)

partial_assistant_message = claude_response_to_function_call + "</function_calls>"
if "<invoke>" in claude_response_to_function_call:
    result = custom_calculator()
        
    # Format the function results
    function_results = f"""<function_results>
        <result>
            <tool_name>custom_calculator</tool_name>
            <stdout>
                {result}
            </stdout>
        </result>
    </function_results>"""
    
    partial_assistant_message += function_results

updated_system_prompt = f"""{system_prompt}
Here is the result of the function call:
{partial_assistant_message}
Based on this result, please provide a response to the original question. If custom_calculator is used, just state the answer. Do NOT mention custom calculator in the final answer.
"""
print(f"updated_system_prompt: {updated_system_prompt}")

final_message = client.messages.create(
    model=MODEL_NAME,
    max_tokens=1000,
    messages=[user_message],
    system=updated_system_prompt
).content[0].text
print(f"final_message: {final_message}")

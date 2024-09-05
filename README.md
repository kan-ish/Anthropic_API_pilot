# Setup
### Get the code
   * Fork the repository and clone it OR
   * Download the project as zip. 
### Create a virtual environment
   1. `python -m venv venv`
   2. `source venv/bin/activate` if you're on Linux/MacOS
   `venv\Scripts\activate` if you're on Windows 
### Install dependencies with 
   * `pip install -r requirements.txt`
### API key
  * Create a `.env` file in the root folder of the project.
  * Provide your Anthropic API key as `CLAUDE_API_KEY=$YOUR_API_KEY`\
_Note: This project generates ~900 tokens for the first few messages in a conversation and can go over 4000 tokens for conversations 15+ messages long_
### Create db file with `touch blogs.db` in the task2 folder
### Navigate to task1 or task2
### Run `python3 main.py` or `python main.py`

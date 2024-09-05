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
  * Provide your Anthropic API key as `CLAUDE_API_KEY=$YOUR_API_KEY`
This project generate ~ 900 tokens for smaller queries and can go up to 4000 tokens for conversations 15+ messages long

### Navigate to task1 or task2
### Run `python3 main.py` or `python main.py`

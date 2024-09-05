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
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "Unique id of the article in the database." 
                    },
                },
                "required": ["id"]
            }
        }
    ]
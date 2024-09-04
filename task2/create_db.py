import sqlite3
import os

# Connect to the SQLite database (or create it if it doesn't exist)
db_path = os.path.join(".", "blogs.db")
conn = sqlite3.connect(db_path)

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create the articles table
cursor.execute('''
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    content TEXT,
    date_published TEXT
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Table 'articles' created successfully in blogs.db")

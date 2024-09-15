import sqlite3

connection = sqlite3.connect('prompts.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO prompts (content, category) VALUES (?, ?)",
            ('Write a blog post about...', 'Marketing')
            )

cur.execute("INSERT INTO prompts (content, category) VALUES (?, ?)",
            ('Generate Python code for...', 'Coding')
            )

cur.execute("INSERT INTO prompts (content, category) VALUES (?, ?)",
            ('Create an AI model that...', 'AI')
            )

connection.commit()
connection.close()
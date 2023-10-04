import sqlite3

def initialize_database():
    # Create or connect to your database in the \data directory
    with sqlite3.connect('data/web_crawling.db') as conn:
        cursor = conn.cursor()

        # Define database schema with a more informative table name and an additional column
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS robots_txt_data (
                id INTEGER PRIMARY KEY,
                url TEXT UNIQUE,
                date_crawled TEXT,
                robots_txt_content TEXT
            )
        ''')

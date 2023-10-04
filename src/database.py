# database.py
from datetime import datetime
import sqlite3


def initialize_database():
    """
    Connects to the 'data/web_crawling.db' database and creates the 'robots_txt_data' table if it does not exist.
    """
    database_path = 'data/web_crawling.db'
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS robots_txt_data (
            id INTEGER PRIMARY KEY,
            url TEXT UNIQUE,
            date_crawled TEXT,
            robots_txt_content TEXT,
            disallowed_paths TEXT,
            crawl_delay TEXT,
            sitemap_urls TEXT
        )
    '''

    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        cursor.execute(create_table_query)


def store_website_data(url, robots_txt_data):
    """
    Store website data in the database if it doesn't already exist.
    Args:
        url (str): The URL of the website.
        robots_txt_data (dict): The data of the robots.txt file.
    Returns:
        None
    """
    with sqlite3.connect('data/web_crawling.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM robots_txt_data WHERE url = ?', (url,))
        existing_website = cursor.fetchone()

        if existing_website:
            print(f"Website '{url}' already crawled. Skipping...")
        else:
            cursor.execute(
                'INSERT INTO robots_txt_data (url, date_crawled, robots_txt_content, disallowed_paths, crawl_delay, '
                'sitemap_urls) VALUES (?, ?, ?, ?, ?, ?)',
                (url, datetime.now(), robots_txt_data['content'], robots_txt_data['disallowed_paths'],
                 robots_txt_data['crawl_delay'], robots_txt_data['sitemap_urls'],))
            print(f"Website '{url}' crawled, and robots.txt content stored.")

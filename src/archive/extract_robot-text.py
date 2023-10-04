import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
from urllib.robotparser import RobotFileParser

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

def store_website(url):
    with sqlite3.connect('data/web_crawling.db') as conn:
        cursor = conn.cursor()

        # Check if the website already exists
        cursor.execute('SELECT id FROM robots_txt_data WHERE url = ?', (url,))
        existing_website = cursor.fetchone()

        if existing_website:
            print(f"Website '{url}' already crawled. Skipping...")
        else:
            try:
                # Check if the website allows web crawlers to access its robots.txt file
                rp = RobotFileParser()
                rp.set_url(f"{url}/robots.txt")
                rp.read()
                if not rp.can_fetch("*", f"{url}/robots.txt"):
                    print(f"Website '{url}' does not allow web crawlers to access its robots.txt file. Skipping...")
                    return

                # Crawl the website and store the raw content of the robots.txt file
                headers = {'User-Agent': 'Mozilla'}
                response = requests.get(url, headers=headers)
                robots_txt_content = response.text

                # Store website information including the raw robots.txt content in the database
                cursor.execute('INSERT INTO robots_txt_data (url, date_crawled, robots_txt_content) VALUES (?, ?, ?)', (url, datetime.now(), robots_txt_content,))
                print(f"Website '{url}' crawled, and robots.txt content stored.")
            except Exception as e:
                print(f"Error crawling website '{url}': {e}")

def store_websites(websites):
    with sqlite3.connect('data/web_crawling.db') as conn:
        cursor = conn.cursor()

        # Prepare data for bulk insert
        data = []
        for website in websites:
            cursor.execute('SELECT id FROM robots_txt_data WHERE url = ?', (website,))
            existing_website = cursor.fetchone()
            if not existing_website:
                # Check if the website allows web crawlers to access its robots.txt file
                rp = RobotFileParser()
                rp.set_url(f"{website}/robots.txt")
                rp.read()
                if not rp.can_fetch("*", f"{website}/robots.txt"):
                    print(f"Website '{website}' does not allow web crawlers to access its robots.txt file. Skipping...")
                    continue
                data.append((website, datetime.now()))

        # Crawl websites and store data in bulk
        for url in data:
            try:
                headers = {'User-Agent': 'Mozilla'}
                response = requests.get(url[0], headers=headers)
                robots_txt_content = response.text
                data[data.index(url)] += (robots_txt_content,)
            except Exception as e:
                print(f"Error crawling website '{url[0]}': {e}")
                data.remove(url)

        cursor.executemany('INSERT INTO robots_txt_data (url, date_crawled, robots_txt_content) VALUES (?, ?, ?)', data)
        print(f"{len(data)} websites crawled and robots.txt content stored.")

# Test the implementation
initialize_database()
websites = ['https://www.google.com', 'https://www.facebook.com', 'https://www.amazon.com']
store_websites(websites)

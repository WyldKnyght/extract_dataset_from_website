from datetime import datetime
from crawler import check_website_crawl_permission, crawl_website
import database
import sqlite3

def store_website_data(url, robots_txt_content):
    database.initialize_database()
    
    with sqlite3.connect('data/web_crawling.db') as conn:
        cursor = conn.cursor()

        # Check if the website already exists
        cursor.execute('SELECT id FROM robots_txt_data WHERE url = ?', (url,))
        existing_website = cursor.fetchone()

        if existing_website:
            print(f"Website '{url}' already crawled. Skipping...")
        else:
            # Store website information including the raw robots.txt content in the database
            cursor.execute('INSERT INTO robots_txt_data (url, date_crawled, robots_txt_content) VALUES (?, ?, ?)', (url, datetime.now(), robots_txt_content,))
            print(f"Website '{url}' crawled, and robots.txt content stored.")

def main():
    websites = ['https://www.google.com', 'https://www.facebook.com', 'https://www.amazon.com']
    
    for website in websites:
        if check_website_crawl_permission(website):
            robots_txt_content = crawl_website(website)
            if robots_txt_content is not None:
                store_website_data(website, robots_txt_content)
        else:
            print(f"Website '{website}' does not allow web crawlers to access its robots.txt file. Skipping...")

if __name__ == "__main__":
    main()

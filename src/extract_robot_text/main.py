# main.py
import os
from crawler import Crawler

# Define the database file path
database_file = '../../data/web_crawling.db'

# Define the absolute path to websites_to_scrape.txt in the project's root directory
websites_file_path = '../../websites_to_scrape.txt'


def main():
    # Create the Crawler instance
    crawler = Crawler(database_file)

    if os.path.exists(websites_file_path):
        # Open and read the websites from the file
        with open(websites_file_path, 'r') as file:
            websites = [line.strip() for line in file.readlines()]

        # Loop through the list of websites and process each one
        for website_url in websites:
            # Check if the website is allowed by robots.txt
            if crawler.is_allowed_by_robots(website_url):
                # Store the robots.txt data in the database
                crawler.store_robots_txt(website_url)
                print(f"Website '{website_url}' successfully crawled and data stored.")
            else:
                print(f"Website '{website_url}' does not allow web crawlers. Skipping...")
    else:
        print(f"Websites file '{websites_file_path}' not found.")


if __name__ == '__main__':
    main()

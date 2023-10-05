# main.py
from crawler import Crawler
import database
import logging

def read_websites_from_file(file_path):
    """
    Read a list of websites from a text file.
    Args:
        file_path (str): The path to the text file containing the list of websites.
    Returns:
        list: A list of website URLs.
    """
    with open(file_path, 'r') as file:
        websites = [line.strip() for line in file.readlines()]
    return websites

def crawl_websites_from_file():
    """
    Function that crawls websites listed in a text file and stores the robots.txt data in the database.

    Parameters:
    - None

    Returns:
    None
    """
    # Create an instance of the Crawler class
    crawler = Crawler()

    # Set up logging
    logging.basicConfig(filename='crawler.log', level=logging.INFO)

    # Read websites from the file
    websites_file_path = 'websites_to_scrape.txt'  # Replace with the actual path to your file
    websites = read_websites_from_file(websites_file_path)

    # Iterate over each website in the list
    for website in websites:
        try:
            # Check if the website allows web crawlers to access its robots.txt file
            if crawler.check_website_crawl_permission(website):
                # Crawl the website and get the robots.txt data
                robots_txt_data = crawler.crawl_website(website)
                # Store the website data in the database if the robots.txt data is not None
                if robots_txt_data is not None:
                    database.store_website_data(website, robots_txt_data)
                    print(f"Website '{website}' crawled and data stored successfully.")
                else:
                    print(f"Website '{website}' does not have robots.txt data.")
            else:
                # Skip websites that do not allow web crawlers to access their robots.txt file
                print(f"Website '{website}' does not allow web crawlers. Skipping...")
        except Exception as e:
            # Log any exceptions that occur during the crawling process
            logging.error(f'Error crawling website {website}: {e}')
            print(f"Error crawling website '{website}': {e}")

if __name__ == "__main__":
    # Initialize the database
    database.initialize_database()

    # Crawl websites from the file
    crawl_websites_from_file()

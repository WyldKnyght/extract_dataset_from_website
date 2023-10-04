# main.py
from crawler import Crawler
import database


def crawl_websites(websites):
    """
    Function that crawls a list of websites and stores the robots.txt data in the database.

    Parameters:
    - websites: List of websites to crawl

    Returns:
    None
    """

    # Create an instance of the Crawler class
    crawler = Crawler()

    # Iterate over each website in the list
    for website in websites:
        # Check if the website allows web crawlers to access its robots.txt file
        if crawler.check_website_crawl_permission(website):
            # Crawl the website and get the robots.txt data
            robots_txt_data = crawler.crawl_website(website)
            # Store the website data in the database if the robots.txt data is not None
            if robots_txt_data is not None:
                database.store_website_data(website, robots_txt_data)
        else:
            # Skip websites that do not allow web crawlers to access their robots.txt file
            pass

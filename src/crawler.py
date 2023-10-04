import requests
from urllib.robotparser import RobotFileParser

def check_website_crawl_permission(url):
    rp = RobotFileParser()
    rp.set_url(f"{url}/robots.txt")
    rp.read()
    return rp.can_fetch("*", f"{url}/robots.txt")

def crawl_website(url):
    try:
        # Crawl the website and return the raw content of the robots.txt file
        headers = {'User-Agent': 'Mozilla'}
        response = requests.get(url, headers=headers)
        return response.text
    except Exception as e:
        print(f"Error crawling website '{url}': {e}")
        return None

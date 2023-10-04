import requests
from urllib.robotparser import RobotFileParser


class Crawler:
    def __init__(self):
        self.robots_parser = RobotFileParser()

    def check_website_crawl_permission(self, url):
        robots_txt_url = f"{url}/robots.txt"
        self.robots_parser.set_url(robots_txt_url)
        self.robots_parser.read()
        return self.robots_parser.can_fetch("*", robots_txt_url)

    def crawl_website(self, url):
        try:
            headers = {'User-Agent': 'Mozilla'}
            response = requests.get(url, headers=headers)

            robots_txt_url = f"{url}/robots.txt"
            self.robots_parser.set_url(robots_txt_url)
            self.robots_parser.read()

            disallowed = not self.robots_parser.can_fetch("*", robots_txt_url)
            crawl_delay = self.robots_parser.crawl_delay("*")
            sitemap_urls = self.robots_parser.site_maps()

            return {
                'content': response.text,
                'disallowed': disallowed,
                'crawl_delay': crawl_delay,
                'sitemap_urls': sitemap_urls
            }
        except requests.exceptions.RequestException as e:
            print(f"Error crawling website '{url}': {e}")
            return None

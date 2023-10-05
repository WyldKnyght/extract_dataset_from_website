import requests
from urllib.robotparser import RobotFileParser


class Crawler:
    def __init__(self):
        self.session = requests.Session()
        self.robots_parser = RobotFileParser()

    def check_website_crawl_permission(self, url):
        robots_txt_url = f"{url}/robots.txt"
        self.robots_parser.set_url(robots_txt_url)
        self.robots_parser.read()
        return self.robots_parser.can_fetch("*", url)

    def crawl_website(self, url):
        headers = {'User-Agent': 'Mozilla'}
        response = self.session.get(url, headers=headers)
        response.raise_for_status()

        disallowed = not self.robots_parser.can_fetch("*", url)
        crawl_delay = self.robots_parser.crawl_delay("*") or 0
        sitemap_urls = self.robots_parser.site_maps()

        return {
            'content': response.content,
            'disallowed': disallowed,
            'crawl_delay': crawl_delay,
            'sitemap_urls': sitemap_urls
        }
# crawler.py
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

def crawl_website(self, url):
    headers = {'User-Agent': 'Mozilla'}
    response = self.session.get(url, headers=headers)
    response.raise_for_status()

    robots_txt_url = f"{url}/robots.txt"
    self.robots_parser.set_url(robots_txt_url)
    self.robots_parser.read()

    disallowed = not self.robots_parser.can_fetch("*", url)
    crawl_delay = self.robots_parser.crawl_delay("*") or 0
    sitemap_urls = self.robots_parser.site_maps()

    # Get the parsed rules
    parsed_rules = []
    for entry in self.robots_parser.entries:
        parsed_rules.append({
            'user_agent': entry.user_agent,
            'rule_lines': [str(rule_line) for rule_line in entry.rule_lines]
        })

    # Debog Print
    print(f"Parsed rules for {url}:")
    for rule in parsed_rules:
        print(f"User-agent: {rule['user_agent']}")
        for rule_line in rule['rule_lines']:
            print(f"Rule line: {rule_line}")

    return {
        'content': response.content,
        'disallowed': disallowed,
        'crawl_delay': crawl_delay,
        'sitemap_urls': sitemap_urls,
        'parsed_rules': parsed_rules  # Add the parsed rules to the dictionary
    }


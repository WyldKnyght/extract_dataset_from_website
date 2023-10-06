# crawler.py
import requests
import io
from bs4 import BeautifulSoup
import sqlite3
from urllib.parse import urlparse
import os


class Crawler:
    def __init__(self, db_file):
        self.session = requests.Session()
        self.robots_parser = None
        self.db_file = os.path.abspath(db_file)  # Convert to an absolute path
        self.create_table()

    def create_table(self):
        if not os.path.exists(self.db_file):
            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
            # Create an empty database file
            open(self.db_file, 'a').close()

        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS robots (
                        id INTEGER PRIMARY KEY,
                        domain TEXT,
                        user_agent TEXT,
                        rule TEXT,
                        allow INTEGER,
                        crawl_delay REAL,
                        sitemap TEXT
                    )''')
        conn.commit()
        conn.close()

    def store_robots_txt(self, url):
        headers = {'User-Agent': 'Mozilla'}
        try:
            response = self.session.get(url + '/robots.txt', headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                # Assume all URLs are allowed if there is no robots.txt file
                return
            else:
                raise e

        # Use io.BytesIO to create a file-like object from response.content
        f = io.BytesIO(response.content)
        soup = BeautifulSoup(f, 'html.parser')

        parsed = urlparse(url)
        domain = parsed.netloc

        user_agent = ''
        rules = []
        allow = True
        crawl_delay = None
        sitemap_urls = []

        for line in soup.text.split('\n'):
            if line.startswith('User-agent:'):
                user_agent = line.split(': ')[1]
                allow = True  # Initialize "allow" to True
                crawl_delay = None
            elif line.startswith('Disallow:'):
                path_rule = line.split(': ')[1]
                # Determine if site has a disallow or allow rule
                if path_rule.startswith('/'):
                    rules.append((user_agent, path_rule, False))  # Disallow rule
                else:
                    rules.append((user_agent, path_rule, True))  # Allow rule
            elif line.startswith('Crawl-delay:'):
                crawl_delay = float(line.split(': ')[1])
            elif line.startswith('Sitemap:'):
                sitemap_urls.append(line.split(': ')[1])

        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        for rule in rules:
            c.execute('''INSERT INTO robots (domain, user_agent, rule, allow, crawl_delay, sitemap)
                          VALUES (?, ?, ?, ?, ?, ?)''',
                      (domain, rule[0], rule[1], rule[2], crawl_delay, ','.join(sitemap_urls)))
        conn.commit()
        conn.close()

    def get_robots_parser(self, url):
        if self.robots_parser is None:
            self.robots_parser = {}
        if url not in self.robots_parser:
            self.robots_parser[url] = self.parse_robots_txt(url + '/robots.txt')
        return self.robots_parser[url]

    def parse_robots_txt(self, url):
        headers = {'User-Agent': 'Mozilla'}
        response = self.session.get(url, headers=headers)
        response.raise_for_status()
        robots_parser = {}
        current_user_agent = None

        for line in response.text.split('\n'):
            if line.startswith('User-agent:'):
                current_user_agent = line.split(': ')[1]
                robots_parser[current_user_agent] = []
            elif line.startswith('Disallow:'):
                robots_parser[current_user_agent].append(line.split(': ')[1])

        return robots_parser

    def is_allowed_by_robots(self, url):
        parsed = urlparse(url)
        domain = parsed.netloc
        path = parsed.path
        try:
            robots_parser = self.get_robots_parser('https://' + domain + '/robots.txt')
        except requests.exceptions.HTTPError:
            # Assume all URLs are allowed if there is no robots.txt file
            return True

        if 'User-agent: *' in robots_parser:
            for rule in robots_parser['User-agent: *']:
                if rule == '/' or path.startswith(rule):
                    return False

        if 'User-agent: Mozilla' in robots_parser:
            for rule in robots_parser['User-agent: Mozilla']:
                if rule == '/' or path.startswith(rule):
                    return False

        return True

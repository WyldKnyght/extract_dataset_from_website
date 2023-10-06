# database.py
import sqlite3


class Database:
    def __init__(self, db_file):
        self.db_file = db_file

    def create_table(self):
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

    def insert_robots_data(self, domain, user_agent, rule, allow, crawl_delay, sitemap):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''INSERT INTO robots (domain, user_agent, rule, allow, crawl_delay, sitemap)
                      VALUES (?, ?, ?, ?, ?, ?)''',
                  (domain, user_agent, rule, allow, crawl_delay, sitemap))
        conn.commit()
        conn.close()

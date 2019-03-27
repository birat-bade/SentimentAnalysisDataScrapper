import threading

from src.main.utilities.soup import SoupHelper
from src.config.config import Config
from src.main.utilities.logger import Logger

import requests


class URLScrapeThread(threading.Thread):
    def __init__(self, queue, url_list):

        threading.Thread.__init__(self)
        self.lock = threading.Lock()

        self.queue = queue
        self.url_list = url_list

    def run(self):
        while True:
            article_section_url = self.queue.get()
            try:
                self.scrape_article_url(article_section_url)
            finally:
                self.queue.task_done()

    def scrape_article_url(self, article_section_url):
        # Logic goes here
        pass

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
        try:
            soup = SoupHelper.get_url_soup(article_section_url)
            article_soup = soup.findAll('div', {'class': 'teaser offset'})
            for data in article_soup:
                url_soup = SoupHelper.get_txt_soup(data).find('h2')
                url_soup = SoupHelper.get_txt_soup(url_soup).find('a', href=True)
                article_url = url_soup['href']
                article_url = Config.kantipur_daily_url + article_url.strip()

                self.url_list.append(article_url)

        except TimeoutError:
            Logger.add_error('TimeoutError ' + article_section_url)

        except requests.ConnectionError:
            Logger.add_error('ConnectionError ' + article_section_url)

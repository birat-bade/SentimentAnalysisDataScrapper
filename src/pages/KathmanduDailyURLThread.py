import threading

from src.main.utilities.soup import SoupHelper
from src.config.config import Config
from src.main.utilities.logger import Logger

import requests


class URLScrapeThread(threading.Thread):
    def __init__(self, page_url):

        threading.Thread.__init__(self)

        self.lock = threading.Lock()

        self.page_url = page_url

        self.article_url_list = list()

    def run(self):
        self.lock.acquire()
        self.scrape_article_url()
        self.lock.release()

    def scrape_article_url(self):
        try:
            soup = SoupHelper.get_url_soup(self.page_url)
            article_soup = soup.findAll('div', {'class': 'teaser offset'})
            for data in article_soup:
                url_soup = SoupHelper.get_txt_soup(data).find('h2')
                url_soup = SoupHelper.get_txt_soup(url_soup).find('a', href=True)
                article_url = url_soup['href']
                article_url = Config.kantipur_daily + article_url.strip()

                self.article_url_list.append(article_url)

        except TimeoutError:
            Logger.add_error('TimeoutError ' + self.page_url)

        except requests.ConnectionError:
            Logger.add_error('ConnectionError ' + self.page_url)

    def get_article_url_list(self):
        return self.article_url_list

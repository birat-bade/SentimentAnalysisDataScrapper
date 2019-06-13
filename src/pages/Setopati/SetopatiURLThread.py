import threading

import requests

from src.config.config import Config
from src.main.utilities.logger import Logger
from src.main.utilities.soup import SoupHelper


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

            md_4 = soup.findAll('div', {'class': 'items col-md-4'})
            md_6 = soup.findAll('div', {'class': 'items col-md-6'})

            all_url = list()

            for data in md_4:
                url_soup = SoupHelper.get_txt_soup(data).find('a', href=True)
                all_url.append(url_soup['href'])

            for data in md_6:
                try:
                    url_soup = SoupHelper.get_txt_soup(data).find('a', href=True)
                    all_url.append(url_soup['href'])
                except TypeError:
                    pass
            while '#' in all_url:
                all_url.remove('#')
            while 'https://www.setopati.com' in all_url:
                all_url.remove('https://www.setopati.com')
            while 'http://icc.setopati.com/' in all_url:
                all_url.remove('http://icc.setopati.com/')
            while 'https://www.setopati.com/our-team' in all_url:
                all_url.remove('https://www.setopati.com/our-team')

            for article_url in all_url:
                self.url_list.append(article_url)

        except TimeoutError:
            Logger.add_error('TimeoutError ' + article_section_url)

        except requests.ConnectionError:
            Logger.add_error('ConnectionError ' + article_section_url)

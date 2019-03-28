import threading

from src.db_handler.db_helper import DbHelper
from src.main.utilities.soup import SoupHelper
from src.main.utilities.logger import Logger
from src.config.config import Config

import requests


class DataScrapeThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.queue = queue

    def run(self):
        while True:
            article_url = self.queue.get()
            try:
                scrape_article_data(article_url)
            finally:
                self.queue.task_done()


def scrape_article_data(article_url):
    try:
        db_helper = DbHelper()

        article_url = article_url.split('||||')
        category = article_url[1]
        article_url = article_url[0]

        soup = SoupHelper.get_url_soup(article_url)

        title = soup.find('div', {'class': 'inner-section cover-news'})
        title = SoupHelper.get_txt_soup(title).find('div', {'class': 'col-sm-12'})
        title = SoupHelper.get_txt_soup(title).find('h1')

        if title is None:
            Logger.add_error('Dead Link ' + str(article_url))
            return

        title = title.text

        date = soup.find('div', {'class', 'author-location'})
        date = SoupHelper.get_txt_soup(date).find('span')
        date = date.text.split(',')
        date = date[1].strip().split(' ')
        month = date[1]
        day = date[0]
        year = date[2]
        date = str(month) + ' ' + str(day) + ',' + str(year)

        article = soup.find('div', {'id': 'newsContent'})
        article = SoupHelper.get_txt_soup(article).findAll('p')

        article_text = list()
        for data in article:
            article_text.append(data.text.strip())
        article_text = ''.join(article_text)

        db_helper.insert_article(article_url, Config.nagarik_news,
                                 Config.nagarik_news_sections_dict.get(category), title, date,
                                 article_text)
        db_helper.close_connection()

        Logger.add_log('Scrapping : ' + article_url)

    except TimeoutError:
        Logger.add_error('TimeoutError ' + article_url)

    except requests.ConnectionError:
        Logger.add_error('ConnectionError ' + article_url)

import threading

from src.db_handler.db_helper import DbHelper
from src.main.utilities.soup import SoupHelper
from src.main.utilities.logger import Logger
from src.config.config import Config

import requests

from datetime import datetime


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
        db_helper = DbHelper(Config.db_english)

        temp = article_url.split('/')
        category = temp[4]

        if db_helper.data_present(article_url):
            return

        soup = SoupHelper.get_url_soup(article_url)

        title = soup.find('div', {'class': 'col-lg-12'})
        title = SoupHelper.get_txt_soup(title).find('h4')

        if title is None:
            Logger.add_error('Dead Link ' + str(article_url))
            return
        title = title.text

        date = soup.find('div', {'class': 'date-time'})
        date = SoupHelper.get_txt_soup(date).find('span')
        date = date.text
        date = datetime.strptime(date, '%A, %b %d, %Y')
        date = date.strftime('%Y-%m-%d')

        temp_article = soup.find('div', {'class': 'mn-text'})
        temp_article = SoupHelper.get_txt_soup(temp_article).findAll('p')

        article = list()

        for data in temp_article:
            article.append(data.text.strip())

        article = ' '.join(article)

        db_helper.insert_article(article_url, Config.karobar_daily,
                                 category, title, date,
                                 article, '. ')

        db_helper.close_connection()

        Logger.add_log('Scrapping : ' + article_url)

    except TimeoutError:
        Logger.add_error('TimeoutError ' + article_url)

    except requests.ConnectionError:
        Logger.add_error('ConnectionError ' + article_url)

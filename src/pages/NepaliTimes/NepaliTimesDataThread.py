import threading

from src.db_handler.db_helper import DbHelper
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
        db_helper = DbHelper(Config.db_english)

        if db_helper.data_present(article_url):
            return

        # db_helper.insert_article(article_url, Config.kantipur_daily_, category, title, date.text, article)
        db_helper.close_connection()

        Logger.add_log('Scrapping : ' + article_url)

    except TimeoutError:
        Logger.add_error('TimeoutError ' + article_url)

    except requests.ConnectionError:
        Logger.add_error('ConnectionError ' + article_url)

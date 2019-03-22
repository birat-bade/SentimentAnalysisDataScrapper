from src.db_handler.db_helper import DbHelper
from src.pages.KantipurDailyDataThread import DataScrapeThread
from src.pages.KathmanduDailyURLThread import URLScrapeThread
from src.config.config import Config

from queue import Queue

import pandas as pd


class KantipurDaily:
    def __init__(self, date):
        self.date = date
        self.db_helper = DbHelper()

        self.queue = Queue(maxsize=0)

        self.url_threads = list()
        self.data_threads = list()
        self.all_url_list = list()

    def scrape_article_url_initialize(self):
        sections = ['business', 'opinion', 'sports', 'national', 'koseli', 'world', 'entertainment', 'blog', 'diaspora',
                    'feature', 'lifestyle', 'literature', 'technology', 'health', 'pathakmanch', 'Interview', 'Art',
                    'Other', 'nari-nepali']

        for section in sections:
            article_collection = Config.kantipur_daily + '/' + section + '/' + str(self.date)
            thread = URLScrapeThread(article_collection)
            self.url_threads.append(thread)

    def scrape_article_url_execute(self):

        for t in self.url_threads:
            t.start()
        for t in self.url_threads:
            t.join()

        for t in self.url_threads:
            for url in t.get_article_url_list():
                self.all_url_list.append(url)

    def scrape_article_data_initialize(self):

        num_threads = 10

        for i in range(num_threads):
            worker = DataScrapeThread(self.queue)
            worker.setDaemon(True)
            worker.start()

        for url in self.all_url_list:
            if self.db_helper.data_not_present(url):
                self.queue.put(url)

    def scrape_article_data_execute(self):

        self.queue.join()


def scrape(row):
    date = row['date']
    print(date)
    kantipur_daily = KantipurDaily(date)

    kantipur_daily.scrape_article_url_initialize()
    kantipur_daily.scrape_article_url_execute()

    kantipur_daily.scrape_article_data_initialize()
    kantipur_daily.scrape_article_data_execute()
    kantipur_daily.db_helper.close_connection()


if __name__ == '__main__':
    df_input = pd.read_csv(Config.input_kantipur, dtype=object, encoding='ISO-8859-1').fillna('')
    df_input.apply(scrape, 1)

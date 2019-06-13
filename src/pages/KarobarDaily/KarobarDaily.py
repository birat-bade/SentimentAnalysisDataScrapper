import pandas as pd

from queue import Queue

from src.config.config import Config
from src.pages.KarobarDaily.KarobarDailyDataThread import DataScrapeThread
from src.pages.KarobarDaily.KarobarDailyURLThread import URLScrapeThread


class KarobarDaily:
    def __init__(self, page):
        self.page = page

        self.queue_url = Queue(maxsize=0)
        self.queue_data = Queue(maxsize=0)

        self.url_threads = list()
        self.data_threads = list()
        self.all_url_list = list()

    def scrape_article_url_initialize(self):

        num_threads = 20

        for i in range(num_threads):
            worker = URLScrapeThread(self.queue_url, self.all_url_list)
            worker.setDaemon(True)
            worker.start()

        for category in Config.karobar_daily_section:
            article_section = Config.karobar_daily_url + 'news/' + category + '?page=' + str(self.page)
            self.queue_url.put(article_section)

    def scrape_article_url_execute(self):
        self.queue_url.join()

    def scrape_article_data_initialize(self):

        num_threads = 20

        for i in range(num_threads):
            worker = DataScrapeThread(self.queue_data)
            worker.setDaemon(True)
            worker.start()

        for url in self.all_url_list:
            self.queue_data.put(url)

    def scrape_article_data_execute(self):
        self.queue_data.join()


def scrape(row):
    page = row['page']
    print(page)
    karobar_daily = KarobarDaily(page)

    karobar_daily.scrape_article_url_initialize()
    karobar_daily.scrape_article_url_execute()

    karobar_daily.scrape_article_data_initialize()
    karobar_daily.scrape_article_data_execute()


df_input = pd.read_csv(Config.karobar_daily_input, dtype=object, encoding='ISO-8859-1').fillna('')
df_input.apply(scrape, 1)

import pandas as pd

from queue import Queue

from src.config.config import Config
from src.pages.Setopati.SetopatiURLThread import URLScrapeThread
from src.pages.Setopati.SetopatiDataThread import DataScrapeThread


class Setopati:
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

        for category in Config.setopati_sections:
            article_section = Config.setopati_url + category + '?page=' + str(self.page)
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
    setopati = Setopati(page)

    setopati.scrape_article_url_initialize()
    setopati.scrape_article_url_execute()

    setopati.scrape_article_data_initialize()
    setopati.scrape_article_data_execute()


df_input = pd.read_csv(Config.setopati_input, dtype=object, encoding='ISO-8859-1').fillna('')
df_input.apply(scrape, 1)

import pandas as pd

from queue import Queue

from src.config.config import Config
from src.db_handler.db_helper import DbHelper
from src.pages.NagarikNews.NagarikNewsURLThread import URLScrapeThread
from src.pages.NagarikNews.NagarikNewsDataThread import DataScrapeThread


class NagarikNews:
    def __init__(self, page):
        self.page = page
        self.db_helper = DbHelper()

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

        for category in Config.nagarik_news_sections:
            article_section = Config.nagarik_news_url + '/category/' + category + '?page=' + str(self.page)
            self.queue_url.put((article_section, category))

    def scrape_article_url_execute(self):
        self.queue_url.join()

    def scrape_article_data_initialize(self):

        num_threads = 20

        for i in range(num_threads):
            worker = DataScrapeThread(self.queue_data)
            worker.setDaemon(True)
            worker.start()

        for url in self.all_url_list:
            temp = url.split('||||')
            article_url = temp[0]
            if self.db_helper.data_not_present(article_url):
                self.queue_data.put(url)

    def scrape_article_data_execute(self):
        self.queue_data.join()


def scrape(row):
    page = row['page']
    print(page)
    nagarik_news = NagarikNews(page)

    nagarik_news.scrape_article_url_initialize()
    nagarik_news.scrape_article_url_execute()

    nagarik_news.scrape_article_data_initialize()
    nagarik_news.scrape_article_data_execute()


df_input = pd.read_csv(Config.nagarik_news_input, dtype=object, encoding='ISO-8859-1').fillna('')
df_input.apply(scrape, 1)

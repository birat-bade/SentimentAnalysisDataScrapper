import pandas as pd
from queue import Queue

from scrapy.crawler import CrawlerProcess

from src.config.config import Config
from src.db_handler.db_helper import DbHelper
from src.pages.NepaliTimes.NepaliTimesURLThread import URLScrapeThread
from datetime import datetime
from src.main.utilities.logger import Logger
from src.spider.NepaliTimes.NepaliTimes.spiders.nepali_times import NepaliTimesSpider

header = {
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
}


class NepaliTimes:
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

        for section in Config.nepali_times_section:
            article_section = Config.nepali_times_url + 'nt/' + section + '/?page=' + str(self.page)
            self.queue_url.put(article_section)

    def scrape_article_url_execute(self):
        self.queue_url.join()
        return self.all_url_list

    def scrape_article_data_initialize(self):
        pass

    def scrape_article_data_execute(self):
        self.queue_data.join()


def scrape(row):
    page = row['page']
    print(page)
    nepali_times = NepaliTimes(page)

    nepali_times.scrape_article_url_initialize()
    urls = nepali_times.scrape_article_url_execute()

    temp_df = pd.DataFrame(columns=['url'])
    temp_df['url'] = urls

    global output_df
    output_df = output_df.append(temp_df)


def insert_data(row):
    date = row['date']
    date = datetime.strptime(date, '%B %d, %Y')
    date.strftime('%Y-%m-%d')

    url = row['url']
    title = row['title']

    article = row['article']
    category = row['category']
    db_helper = DbHelper(Config.db_english)

    if db_helper.data_present(url):
        return

    db_helper.insert_article(url, Config.nepali_times, category, title, date, article, '. ')
    Logger.add_log('Scrapping : ' + url)


output_df = pd.DataFrame(columns=['url'])

df_input = pd.read_csv(Config.nepali_times_input, dtype=object, encoding='ISO-8859-1').fillna('')
df_input.apply(scrape, 1)

process = CrawlerProcess(header)
process.crawl(NepaliTimesSpider, start_urls=output_df['url'].tolist())
process.start()

df_insert = pd.read_csv(Config.nepali_times_spider_output_location, dtype=object, encoding="ISO-8859-1").fillna('')
df_insert.apply(insert_data, 1)



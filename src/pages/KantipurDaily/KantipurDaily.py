import datetime
from queue import Queue

from src.config.config import Config
from src.pages.KantipurDaily.KantipurDailyDataThread import DataScrapeThread
from src.pages.KantipurDaily.KantipurDailyURLThread import URLScrapeThread


class KantipurDaily:
    def __init__(self, date):
        self.date = date

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

        for section in Config.kantipur_daily_sections:
            article_section = Config.kantipur_daily_url + '/' + section + '/' + str(self.date)
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


def scrape(date):
    # date = row['date']
    print(date)
    kantipur_daily = KantipurDaily(date)

    kantipur_daily.scrape_article_url_initialize()
    kantipur_daily.scrape_article_url_execute()

    kantipur_daily.scrape_article_data_initialize()
    kantipur_daily.scrape_article_data_execute()


# df_input = pd.read_csv(Config.kantipur_daily_input, dtype=object, encoding='ISO-8859-1').fillna('')
# df_input.apply(scrape, 1)

today_date = datetime.datetime.today().strftime('%Y/%m/%d')
scrape(today_date)

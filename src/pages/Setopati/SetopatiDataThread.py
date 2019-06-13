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
        db_helper = DbHelper(Config.db)

        if db_helper.data_present(article_url):
            return

        soup = SoupHelper.get_url_soup(article_url)
        title = soup.find('span', {'class': 'news-big-title'})

        if title is None:
            Logger.add_error('Dead Link ' + str(article_url))
            return

        title = title.text

        article_text = list()

        article = soup.find('div', {'class': 'editor-box'})
        article = SoupHelper.get_txt_soup(article).findAll('p')

        for data in article:
            article_text.append(data.text)

        article_text = ' '.join(article_text)

        pub_date = soup.find('span', {'class': 'pub-date'})

        pub_date = pub_date.text

        month = pub_date.split(',')[1].strip().split(' ')[0]
        day = pub_date.split(',')[1].strip().split(' ')[1]
        year = pub_date.split(',')[2].strip()

        date = str(month) + ' ' + str(day) + ',' + str(year)

        category = article_url.split('/')[3]

        db_helper.insert_article(article_url, Config.setopati, category, title, date, article_text, '।')
        db_helper.close_connection()

        Logger.add_log('Scrapping : ' + article_url)

    except TimeoutError:
        Logger.add_error('TimeoutError ' + article_url)

    except requests.ConnectionError:
        Logger.add_error('ConnectionError ' + article_url)

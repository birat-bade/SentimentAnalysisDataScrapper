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

        title_card = soup.find('div', {'class': 'nws__title--card'})
        title = SoupHelper.get_txt_soup(title_card).find('h2')

        if title is None:
            Logger.add_error('Dead Link ' + str(article_url))
            return

        date = soup.find('div', {'class': 'post__time'})
        date = SoupHelper.get_txt_soup(date).find('span')

        title = title.text
        date = date.text

        date = date.split(' ')
        month = date[1]
        day = date[2]
        year = date[0]

        date = str(month) + ' ' + str(day) + ',' + str(year)

        article = soup.find('div', {'ok__news--wrap'})
        article = SoupHelper.get_txt_soup(article).findAll('p')

        article_text = list()
        for data in article:
            article_text.append(data.text.strip())
        article_text = ''.join(article_text)

        db_helper.insert_article(article_url, Config.online_khabar, category, title, date, article_text)
        db_helper.close_connection()

        Logger.add_log('Scrapping : ' + article_url)

    except TimeoutError:
        Logger.add_error('TimeoutError ' + article_url)

    except requests.ConnectionError:
        Logger.add_error('ConnectionError ' + article_url)

    except requests.TooManyRedirects:
        Logger.add_error('Redirect Error ' + article_url)

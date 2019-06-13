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

        title = soup.find('div', {'class': 'article-header'})
        headline = SoupHelper.get_txt_soup(title).find('h1')
        sub_headline = SoupHelper.get_txt_soup(title).find('div', {'class': 'sub-headline'})

        if title is None:
            Logger.add_error('Dead Link ' + str(article_url))
            return

        title = str(headline.text)

        if sub_headline is not None:
            title = str(headline.text) + '\n' + str(sub_headline.text)

        date = soup.find('time')
        article = soup.find('div', {'class': 'description'})

        scripts = SoupHelper.get_txt_soup(article).findAll('script')
        article = article.text

        for script in scripts:
            script_text = script.text
            if script_text in article:
                article = article.replace(script_text, '')

        article = article.split('Share on Facebook')
        article = article[0]

        temp = article_url.split('/')
        category = temp[3]

        db_helper.insert_article(article_url, Config.kantipur_daily_, category, title, date.text, article, '।')
        db_helper.close_connection()

        Logger.add_log('Scrapping : ' + article_url)

    except TimeoutError:
        Logger.add_error('TimeoutError ' + article_url)

    except requests.ConnectionError:
        Logger.add_error('ConnectionError ' + article_url)

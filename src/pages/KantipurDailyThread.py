import threading

from src.db_handler.db_helper import DbHelper
from src.main.utilities.soup import SoupHelper


class ScrapeThread(threading.Thread):
    def __init__(self, article_url):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.article_url = article_url
        self.db_helper = DbHelper()


    def run(self):
        self.lock.acquire()
        self.scrape_article_data(article_url=self.article_url)
        self.lock.release()

    def scrape_article_data(self, article_url):

        soup = SoupHelper.get_url_soup(article_url)

        print(article_url)

        title = soup.find('div', {'class': 'article-header'})
        headline = SoupHelper.get_txt_soup(title).find('h1')
        sub_headline = SoupHelper.get_txt_soup(title).find('div', {'class': 'sub-headline'})

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

        self.db_helper.insert_article(article_url, title, date.text, article)
        self.db_helper.close_connection()

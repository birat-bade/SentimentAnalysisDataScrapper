from src.db_handler.db_helper import DbHelper
from src.pages.KantipurDailyThread import ScrapeThread
from src.main.utilities.soup import SoupHelper


class KantipurDaily:
    def __init__(self, page_url):
        self.page_url = page_url
        self.db_helper = DbHelper()
        self.parent_url = 'https://www.kantipurdaily.com'

        self.threads = list()

    def scrape_article_url(self):
        soup = SoupHelper.get_url_soup(self.page_url)
        article_soup = soup.findAll('div', {'class': 'teaser offset'})
        for data in article_soup:
            url_soup = SoupHelper.get_txt_soup(data).find('h2')
            url_soup = SoupHelper.get_txt_soup(url_soup).find('a', href=True)
            article_url = url_soup['href']
            article_url = self.parent_url + article_url.strip()

            if self.db_helper.data_not_present(article_url):
                thread = ScrapeThread(article_url=article_url)
                self.threads.append(thread)

    def scrape_article_data(self):
        for t in self.threads:
            # print('start')
            t.start()
        for t in self.threads:
            # print('join')
            t.join()


if __name__ == '__main__':
    kantipur_daily = KantipurDaily('https://www.kantipurdaily.com/news/2019/01/11')
    kantipur_daily.scrape_article_url()
    kantipur_daily.scrape_article_data()
    kantipur_daily.db_helper.close_connection()

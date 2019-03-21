import requests

from bs4 import BeautifulSoup

from src.db_handler.db_helper import DbHelper

headers = {
    'Connection': 'close',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
}


class KantipurDaily:
    def __init__(self, page_url):
        self.page_url = page_url
        self.db_helper = DbHelper()
        self.parent_url = 'https://www.kantipurdaily.com'

    def scrape_article_url(self):
        soup = get_url_soup(self.page_url)
        article_soup = soup.findAll('div', {'class': 'teaser offset'})
        for data in article_soup:
            url_soup = get_txt_soup(data).find('h2')
            url_soup = get_txt_soup(url_soup).find('a', href=True)
            article_url = url_soup['href']

            if self.db_helper.data_not_present(article_url):
                self.scrape_article_data(article_url)

    def scrape_article_data(self, article_url):
        article_url = self.parent_url + article_url.strip()
        soup = get_url_soup(article_url)

        print(article_url)

        title = soup.find('div', {'class': 'article-header'})
        headline = get_txt_soup(title).find('h1')
        sub_headline = get_txt_soup(title).find('div', {'class': 'sub-headline'})

        title = str(headline.text)

        if sub_headline is not None:
            title = str(headline.text) + '\n' + str(sub_headline.text)

        date = soup.find('time')
        article = soup.find('div', {'class': 'description'})

        scripts = get_txt_soup(article).findAll('script')
        article = article.text

        for script in scripts:
            script_text = script.text
            if script_text in article:
                article = article.replace(script_text, '')

        self.db_helper.insert_article(article_url, title, date.text, article)


def get_url_soup(url):
    url_request = requests.get(url, headers=headers, allow_redirects=True)
    soup = BeautifulSoup(url_request.text, 'lxml')
    return soup


def get_txt_soup(text):
    text = str(text)
    soup = BeautifulSoup(text, 'lxml')
    return soup


if __name__ == '__main__':
    kantipur_daily = KantipurDaily('https://www.kantipurdaily.com/news/2019/01/11')
    kantipur_daily.scrape_article_url()
    kantipur_daily.db_helper.close_connection()

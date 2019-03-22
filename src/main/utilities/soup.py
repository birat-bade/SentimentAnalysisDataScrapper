from bs4 import BeautifulSoup
import requests
from src.main.utilities.logger import Logger

headers = {
    'Connection': 'close',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
}


class SoupHelper:
    @staticmethod
    def get_url_soup(url):
        url_request = requests.get(url, headers=headers, allow_redirects=True)
        soup = BeautifulSoup(url_request.text, 'lxml')
        return soup

    @staticmethod
    def get_txt_soup(text):
        text = str(text)
        soup = BeautifulSoup(text, 'lxml')
        return soup

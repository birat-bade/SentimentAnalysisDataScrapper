from bs4 import BeautifulSoup
import requests
from bs4.dammit import EncodingDetector

headers = {
    'Connection': 'close',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',

}


class SoupHelper:
    @staticmethod
    def get_url_soup(url):
        url_request = requests.get(url, headers=headers, allow_redirects=True)
        http_encoding = url_request.encoding if 'charset' in url_request.headers.get('content-type',
                                                                                     '').lower() else None
        html_encoding = EncodingDetector.find_declared_encoding(url_request.content, is_html=True)
        encoding = html_encoding or http_encoding
        soup = BeautifulSoup(url_request.content, 'lxml', from_encoding=encoding)
        return soup

    @staticmethod
    def get_txt_soup(text):
        text = str(text)
        soup = BeautifulSoup(text, 'lxml')
        return soup

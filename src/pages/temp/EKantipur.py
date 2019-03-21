import pandas as pd

import requests

from bs4 import BeautifulSoup

from src.locators.Locators import Locators
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from src.main.utilities.logger import Logger
from src.db_handler.db_helper import DbHelper

headers = {
    'Connection': 'close',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
}


class EKantipur(object):
    def __init__(self, driver):
        self.driver = driver
        self.df = pd.DataFrame()
        self.db_helper = DbHelper()

    def scrape(self):
        self.skip_add()
        self.scrape_articles()
        self.db_helper.close_connection()

    def skip_add(self):
        try:

            WebDriverWait(self.driver, 90).until(
                ec.element_to_be_clickable((By.XPATH, Locators.skip_add_button)))

            button = self.driver.find_element(By.XPATH, Locators.skip_add_button)
            button.click()

        except TimeoutException as e:
            print('timeout')
            Logger.add_error(str(e))

    def scrape_articles(self):
        try:

            soup = get_url_soup(self.driver.current_url)
            tags = soup.findAll('div', {'class': 'total_comments'})

            for url_data in tags:
                url_data = str(url_data).replace('<div class="total_comments" onclick="showFBCommentBox(this,\'', '')
                url_data = str(url_data).replace('\',\'eng\')"><span class="glyphicon glyphicon-comment"></span></div>',
                                                 '')
                title, article = scrape_article_data(url_data)
                self.db_helper.insert_article(url_data, title, article)

        except Exception as e:
            Logger.add_error(str(e))


def scrape_article_data(url_data):
    soup = get_url_soup(url_data)

    title_soup = soup.find('div', {'class': 'titlebar no-space'})
    title_soup = get_txt_soup(title_soup).find('h1').text

    body_soup = soup.findAll('div', {'class': 'content-wrapper '})
    body_soup = get_txt_soup(body_soup).findAll('p')

    temp = list()

    for data in body_soup:
        p_data = data.text.strip()
        if p_data != '':
            temp.append(p_data)

    article = '\n\n'.join(temp)
    article = article[3:]

    return title_soup, article


def get_url_soup(url):
    url_request = requests.get(url, headers=headers, allow_redirects=True)
    soup = BeautifulSoup(url_request.text, 'lxml')
    return soup


def get_txt_soup(text):
    text = str(text)
    soup = BeautifulSoup(text, 'lxml')
    return soup

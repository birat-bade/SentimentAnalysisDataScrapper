# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from src.main.utilities.soup import SoupHelper

from src.config.config import Config


class NepaliTimesSpider(scrapy.Spider):
    name = 'nepali_times'
    allowed_domains = ['https://www.nepalitimes.com/']
    df = pd.DataFrame()

    def parse(self, response):
        soup = SoupHelper.get_url_soup(response.url)

        title = soup.find('div', {'class': 'about-page-detailing'})

        try:
            sub_title = SoupHelper.get_txt_soup(title).find('h5').text
        except AttributeError:
            sub_title = ''

        try:
            title = SoupHelper.get_txt_soup(title).find('h1').text
        except AttributeError:
            title = ''

        title = title + ' ' + sub_title
        title = title.strip()

        date = soup.find('span', {'class': 'dates'})
        date = SoupHelper.get_txt_soup(date).find('a').text
        date = date.strip()

        url = response.url

        article = soup.find('div', {'class': 'elementor-section-wrap'})
        article = SoupHelper.get_txt_soup(article).find_all('p')

        temp = list()

        for p in article:
            data = p.text
            data = data.strip()
            if '(adsbygoogle = window.adsbygoogle || []).push({});' not in data:
                temp.append(data)

        article = ' '.join(temp)
        article = article.strip()

        temp_df = pd.DataFrame()
        temp_df['url'] = [url]
        temp_df['title'] = [title]
        temp_df['date'] = [date]
        temp_df['article'] = [article]
        temp_df['category'] = [url.split('/')[3]]

        self.df = self.df.append(temp_df)
        self.df.to_csv(Config.nepali_times_spider_output_location, index=False)

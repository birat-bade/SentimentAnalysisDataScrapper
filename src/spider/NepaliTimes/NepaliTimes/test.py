from scrapy.crawler import CrawlerProcess

import pandas as pd

from src.spider.NepaliTimes.NepaliTimes.spiders.nepali_times import NepaliTimesSpider

spider = NepaliTimesSpider(domain='https://www.nepalitimes.com/')

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(NepaliTimesSpider, start_urls=pd.read_csv('input.csv', encoding='ISO-8859-1').fillna('')['url'].tolist())
process.start()

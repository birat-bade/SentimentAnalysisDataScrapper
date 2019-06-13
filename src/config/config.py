class Config(object):
    gecko_driver_path = 'src/driver/geckodriver.exe'
    chrome_driver_path = 'src/driver/chromedriver.exe'

    server = 'localhost'
    user = 'root'
    password = ''
    db = 'article_warehouse'
    db_english = 'article_warehouse_english'

    files = 'src/files'
    temp_url = 'src/files/temp/temp_url.csv'
    log_path = 'src/log/logs.log'

    kantipur_daily_input = 'src/files/kantipur/input.csv'
    kantipur_daily_url = 'https://www.kantipurdaily.com'
    kantipur_daily_ = 'Kantipur Daily'
    kantipur_daily_sections = ['news', 'business', 'opinion', 'sports', 'national', 'koseli', 'world', 'entertainment',
                               'blog',
                               'diaspora', 'feature', 'lifestyle', 'literature', 'technology', 'health', 'pathakmanch',
                               'Interview', 'Art',
                               'Other', 'nari-nepali']

    nagarik_news_input = 'src/files/nagarik_news/input_1.csv'
    nagarik_news_url = 'https://nagariknews.nagariknetwork.com'
    nagarik_news = 'Nagarik News'
    nagarik_news_sections = ['21', '22', '24', '25', '26', '27', '28', '33', '31', '81', '82']
    nagarik_news_sections_dict = {'21': 'Politics', '22': 'Business', '24': 'Social', '25': 'Art', '26': 'Sports',
                                  '27': 'World', '28': 'Diaspora', '33': 'Technology', '31': 'Health', '81': 'Opinion',
                                  '82': 'Interview'}

    online_khabar_input = 'src/files/online_khabar/input_1.csv'
    online_khabar_url = 'https://www.onlinekhabar.com'
    online_khabar = 'Online Khabar'
    online_khabar_sections = ['news', 'prabhas-news', 'sports-news', 'ent-news', 'lifestylenews', 'cover-story',
                              'fitness', 'sambandha', 'interior', 'khanpan', 'beauty', 'sex-health',
                              'religionfallow', 'auto', 'tourism', 'eco-policy', 'bank-main', 'biz-talk', 'technology',
                              'corporate',
                              'rojgar']
    online_khabar_section_dict = {'news': 'News',
                                  'prabhas-news': 'Diaspora',
                                  'sports-news': 'Sports',
                                  'merokatha': 'Sports',
                                  'ent-news': 'Entertainment',
                                  'bolly-hollywood': 'Entertainment',
                                  'gassip': 'Entertainment',
                                  'ent-interview': 'Entertainment',
                                  'lifestylenews': 'Lifestyle',
                                  'cover-story': 'Lifestyle',
                                  'fitness': 'Lifestyle',
                                  'sambandha': 'Lifestyle',
                                  'interior': 'Lifestyle',
                                  'khanpan': 'Lifestyle',
                                  'beauty': 'Lifestyle',
                                  'sex-health': 'Lifestyle',
                                  'religionfallow': 'Lifestyle',
                                  'auto': 'Business ',
                                  'tourism': 'Business ',
                                  'eco-policy': 'Business ',
                                  'bank-main': 'Business ',
                                  'biz-talk': 'Business ',
                                  'technology': 'Technology',
                                  'corporate': 'Business',
                                  'rojgar': 'Business'}

    nepali_times_input = 'src/files/nepali_times/input_0.csv'
    nepali_times_url = 'https://www.nepalitimes.com/'
    nepali_times = 'Nepali Times'

    nepali_times_section = ['latest', 'multimedia', 'here-now', 'editorial', 'opinion', 'about-town', 'must-see']

    nepali_times_spider_output_location = 'E:\\Projects\\Python Projects\\SentimentAnalysisDataScrapper\\src\\files\\nepali_times\\spider_output.csv'

    karobar_daily_input = 'src/files/karobar_daily/input.csv'
    karobar_daily_url = 'https://www.english.karobardaily.com/'
    karobar_daily = 'Karobar Daily'

    karobar_daily_section = ['economy', 'banking', 'insurance', 'country', 'politics', 'society', 'development',
                             'opinion', 'interview']

    setopati_input = 'src/files/setopati/input_2.csv'
    setopati_url = 'https://www.setopati.com/'
    setopati = 'Setopati'
    setopati_sections = ['politics', 'provinces', 'social', 'opinion', 'kinmel', 'art', 'sports', 'ghumphir',
                         'blog', 'literature', 'global']

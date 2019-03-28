class Config(object):
    gecko_driver_path = 'src/driver/geckodriver.exe'
    chrome_driver_path = 'src/driver/chromedriver.exe'

    server = 'localhost'
    user = 'root'
    password = ''
    db = 'articlewarehouse'

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

    nagarik_news_input = 'src/files/nagarik_news/input_6.csv'
    nagarik_news_url = 'https://nagariknews.nagariknetwork.com'
    nagarik_news = 'Nagarik News'
    nagarik_news_sections = ['21', '22', '24', '25', '26', '27', '28', '33', '31', '81', '82']
    nagarik_news_sections_dict = {'21': 'Politics', '22': 'Business', '24': 'Social', '25': 'Art', '26': 'Sports',
                                  '27': 'World', '28': 'Diaspora', '33': 'Technology', '31': 'Health', '81': 'Opinion',
                                  '82': 'Interview'}

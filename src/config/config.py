class Config(object):
    gecko_driver_path = '../../driver/geckodriver.exe'
    chrome_driver_path = '../../driver/chromedriver.exe'

    server = 'localhost'
    user = 'root'
    password = ''
    db = 'articlewarehouse'

    files = '../files/'
    temp_url = '../files/temp/temp_url.csv'
    log_path = 'F:/Projects/Python Projects/Ekantipur Scrapper/src/log/logs.log'

    kantipur_daily_input = '../files/kantipur/input_10.csv'
    kantipur_daily_url = 'https://www.kantipurdaily.com'
    kantipur_daily_ = 'Kantipur Daily'
    kantipur_daily_sections = ['news', 'business', 'opinion', 'sports', 'national', 'koseli', 'world', 'entertainment',
                               'blog',
                               'diaspora', 'feature', 'lifestyle', 'literature', 'technology', 'health', 'pathakmanch',
                               'Interview', 'Art',
                               'Other', 'nari-nepali']

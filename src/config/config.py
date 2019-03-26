class Config(object):
    gecko_driver_path = 'src/driver/geckodriver.exe'
    chrome_driver_path = 'src/driver/chromedriver.exe'

    server = 'localhost'
    user = 'root'
    password = ''
    db = 'article_warehouse'

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

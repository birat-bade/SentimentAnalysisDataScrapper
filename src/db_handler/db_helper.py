import MySQLdb
from src.config.config import Config
from src.main.utilities.logger import Logger


class DbHelper:
    def __init__(self):
        connection = MySQLdb.connect(Config.server, Config.user, Config.password, Config.db, use_unicode=True,
                                     charset="utf8")
        self.connection = connection

    def insert_article(self, article_url, title, date, article):
        try:
            cursor = self.connection.cursor()

            sql = 'insert into articles (article_link,title,date,article) values (%s,%s,%s,%s)'
            cursor.execute(sql, [str(article_url), str(title), str(date), str(article)])
            self.connection.commit()
            del cursor

        except Exception as e:
            Logger.add_error(str(e) + ' ' + str(article_url))

    def data_not_present(self, article_url):
        try:
            cursor = self.connection.cursor()

            sql = 'select * from articles where article_link = %s'

            cursor.execute(sql, [article_url])
            data = cursor.fetchall()

            if len(data) > 0:
                return False
            return True

        except Exception as e:
            Logger.add_error(str(e))

    def close_connection(self):
        self.connection.close()

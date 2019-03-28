import MySQLdb
from src.config.config import Config
from src.main.utilities.logger import Logger


class DbHelper:
    def __init__(self):
        connection = MySQLdb.connect(Config.server, Config.user, Config.password, Config.db, use_unicode=True,
                                     charset="utf8")
        self.connection = connection

    def insert_article(self, article_url, source, category, title, date, article):
        try:
            cursor_article = self.connection.cursor()

            sql = 'insert into articles (article_url,article_source,category,title,date,article) values (%s,%s,%s,%s,%s,%s)'
            cursor_article.execute(sql,
                                   [str(article_url), str(source), str(category), str(title), str(date), str(article)])

            del cursor_article

            cursor_article_sentence = self.connection.cursor()
            sql = 'select article_id from articles where article_url = %s'

            cursor_article_sentence.execute(sql, [article_url])
            data = cursor_article_sentence.fetchone()

            article_id = data[0]
            article_sentences = article.split('।')

            while ' ' in article_sentences:
                article_sentences.remove(' ')

            while '' in article_sentences:
                article_sentences.remove('')

            for sentence in article_sentences:
                cursor_sentence = self.connection.cursor()

                sql = 'insert into article_sentences (article_id,article_sentence) values (%s,%s)'
                cursor_sentence.execute(sql, [str(article_id), str(sentence)])

                del cursor_sentence
            self.connection.commit()
            del cursor_article_sentence

        except Exception as e:
            self.connection.rollback()
            Logger.add_error(str(e) + ' ' + str(article_url))

    def data_not_present(self, article_url):
        try:
            cursor = self.connection.cursor()

            sql = 'select * from articles where article_url = %s'

            cursor.execute(sql, [article_url])
            data = cursor.fetchall()

            if len(data) > 0:
                Logger.add_log('Link already scrapped : ' + article_url)
                return False

            return True

        except Exception as e:
            Logger.add_error(str(e))

    def close_connection(self):
        self.connection.close()

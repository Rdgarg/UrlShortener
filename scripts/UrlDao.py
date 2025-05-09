import logging
from google.cloud import logging as google_cloud_logging
logging_client = google_cloud_logging.Client()
logging_client.setup_logging()  # Automatically configures handlers based on the environment

logger = logging.getLogger(__name__)

class UrlDao:
    def __init__(self, mysql):
        self.mysql = mysql

    def getUrlInfo(self, shorten_url):
        cursor = self.mysql.connection.cursor()
        result = cursor.execute('''SELECT short_url, actual_url FROM Url WHERE short_url = %s''', [shorten_url])
        rc = cursor.rowcount
        logger.info(rc)
        x = cursor.fetchall()
        logger.info(x)
        cursor.close()

        if len(x) == 0:
            return None

        return x[0][1]

    def putUrl(self, shorten_url, actual_url, current_time):
        cursor = self.mysql.connection.cursor()
        result = cursor.execute('''INSERT INTO Url VALUES(%s, %s, %s)''', [shorten_url, actual_url, current_time])
        self.mysql.connection.commit()
        cursor.close()
        return str(result)

    def get_stats(self):
        cursor = self.mysql.connection.cursor()
        result = cursor.execute('''SELECT u.url, u.counter, ur.current_time from url_stats u join Url ur on ur.shorten_url = u.url order by counter desc limit 1000''')
        rc = cursor.rowcount
        logger.info(rc)
        x = cursor.fetchall()
        logger.info(x)
        cursor.close()
        return str(x)

    def get_stats_for_single_url(self, url):
        cursor = self.mysql.connection.cursor()
        result = cursor.execute('''SELECT u.url, u.counter, ur.current_time from url_stats u join Url ur on ur.shorten_url = u.url where u.url = %s''', [url])
        rc = cursor.rowcount
        logger.info(rc)
        x = cursor.fetchall()
        logger.info(x)
        cursor.close()
        return str(x)

    def updateUrlStats(self, url):
        cursor = self.mysql.connection.cursor()

        hits = self.getUrlStats(url)
        logger.info("hits are ", hits)

        if hits == 0:
            a = cursor.execute('''INSERT INTO url_stats VALUES(%s, %s)''', [url, 0])
            self.mysql.connection.commit()

        result = cursor.execute('''UPDATE url_stats SET counter = %s WHERE url = %s''', [hits+1,url])

        self.mysql.connection.commit()
        cursor.close()
        return str(result)

    def getUrlStats(self, url):
        cursor = self.mysql.connection.cursor()
        result = cursor.execute('''SELECT url, counter from url_stats where url = %s''', [url])
        rc = cursor.rowcount
        logger.info(rc)
        x = cursor.fetchall()
        logger.info(x)
        cursor.close()

        if(len(x) == 0):
            return 0

        return x[0][1]

class UrlDao:
    def __init__(self, mysql):
        self.mysql = mysql

    def getUrlInfo(self, shorten_url):
        cursor = self.mysql.connection.cursor()
        result = cursor.execute('''SELECT short_url, actual_url FROM Url WHERE short_url = %s''', [shorten_url])
        rc = cursor.rowcount
        print(rc)
        x = cursor.fetchall()
        print(x)
        # data = result.fetchone()
        cursor.close()

        return str(result)
        # if data is None:
        #     print("mapping doesn't exist")
        #     return None
        # else:
        #     print(data)
        #     return data

    def putUrl(self, shorten_url, actual_url):
        cursor = self.mysql.connection.cursor()
        result = cursor.execute('''INSERT INTO Url VALUES(%s, %s)''', [shorten_url, actual_url])
        self.mysql.connection.commit()
        cursor.close()
        return str(result)

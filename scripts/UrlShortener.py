import string
import random
import time


class UrlShortener:
    def __init__(self, urlDao):
        self.urlDao = urlDao

    url_dict = {}

    def urlshortener(self, url):
        # time.sleep(random.random())
        letters = string.ascii_lowercase
        shortened_url = ''.join(random.choice(letters) for i in range(6))
        shortened_url = 'https://' + shortened_url

        if self.urlDao.getUrlInfo(shortened_url) is not None:
            print("The shortened URL %s already exists,", shortened_url)
            return self.urlshortener(url)

        self.urlDao.putUrl(shortened_url, url)
        return shortened_url

    def getActualUrl(self, shortened_url):
        urlinfo = self.urlDao.getUrlInfo(shortened_url)
        if urlinfo is None:
            return "URL not found"
        return urlinfo

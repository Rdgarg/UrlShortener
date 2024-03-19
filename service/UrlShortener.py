import string
import random


class UrlShortener:
    def __init__(self, urlDao):
        self.urlDao = urlDao

    url_dict = {}

    def urlshortener(self, url):
        letters = string.ascii_lowercase
        shortened_url = ''.join(random.choice(letters) for i in range(6))
        shortened_url = 'https://' + shortened_url
        return self.urlDao.putUrl(shortened_url, url)

    def getActualUrl(self, shortened_url):
        urlinfo = self.urlDao.getUrlInfo(shortened_url)
        return urlinfo
        # if shortened_url in url_dict.keys():
        #     return url_dict[shortened_url]
        # return "URL not found"

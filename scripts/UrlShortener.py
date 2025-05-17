import json
import random
import validators
import hashlib
import base64
import datetime

URL_PREFIX = "https://my-short-url.com/route/"

import logging # Automatically configures handlers based on the environment

logger = logging.getLogger(__name__)


def get_random_url_suffix(url):
    md5_hash = hashlib.md5(url.encode("utf-8")).hexdigest()
    base64_bytes = base64.b64encode(md5_hash.encode("ascii"))
    base64_string = base64_bytes.decode("ascii")
    shuffled_string = ''.join(random.sample(base64_string,len(base64_string)))
    return shuffled_string[0:7]


class UrlShortener:
    def __init__(self, urlDao):
        self.urlDao = urlDao

    url_dict = {}

    def urlshortener(self, url, user_id, ip):
        if not validators.url(url):
            logger.info("Invalid URL", url)
            raise Exception("Invalid URL")
        # time.sleep(random.random())
        url_suffix = get_random_url_suffix(url)
        logger.info("got url suffix", url_suffix)
        # letters = string.ascii_lowercase
        # shortened_url = ''.join(random.choice(letters) for i in range(6))
        shortened_url = URL_PREFIX + url_suffix

        if self.urlDao.getUrlInfo(url_suffix) is not None:
            logger.info("The shortened URL %s already exists,", shortened_url)
            return self.urlshortener(url, user_id, ip)

        self.urlDao.putUrl(url_suffix, url,datetime.datetime.now(), user_id, ip )
        return shortened_url

    def getActualUrl(self, shortened_url):
        if not shortened_url.startswith(URL_PREFIX):
            logger.info("Invalid URL", shortened_url)
            raise Exception("Invalid URL")

        urlinfo = self.urlDao.getUrlInfo(shortened_url[len(URL_PREFIX):])
        if urlinfo is None:
            return "URL not found"
        self.urlDao.updateUrlStats(shortened_url[len(URL_PREFIX):])
        return urlinfo

    def get_actual_url_without_prefix(self, shortened_url):

        urlinfo = self.urlDao.getUrlInfo(shortened_url)
        if urlinfo is None:
            return "URL not found"
        self.urlDao.updateUrlStats(shortened_url)
        return urlinfo

    def get_stats(self):
        url_stats =  self.urlDao.get_stats()
        for stats in url_stats:
            stats["short_url"] = URL_PREFIX + stats["short_url"]

        return json.dumps(url_stats)

    def get_stats_for_single_url(self, url):
        url_suffix = url[len(URL_PREFIX):]
        url_stats =  self.urlDao.get_stats_for_single_url(url_suffix)
        for stats in url_stats:
            stats["short_url"] = URL_PREFIX + stats["short_url"]

        return json.dumps(url_stats)

    def get_user_info(self, user_id):
        user_info = self.urlDao.get_user_info(user_id)
        if user_info is None:
            logger.info("User not found", user_id)
            return None
        return user_info

    def add_user_info(self, user_id, email, name):
        if self.get_user_info(user_id) is not None:
            logger.info("User already exists", user_id)
            return None
        return self.urlDao.add_user_info(user_id, email, name, datetime.datetime.now())

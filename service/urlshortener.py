import string
import random

url_dict = {}


def urlshortener(url):
    if url in url_dict:
        return url_dict[url]
    letters = string.ascii_lowercase
    shortened_url = ''.join(random.choice(letters) for i in range(6))
    shortened_url = 'https://' + shortened_url
    url_dict[url] = shortened_url
    return shortened_url


def getActualUrl(shortened_url):
    if shortened_url in url_dict.keys():
        return url_dict[shortened_url]
    return "URL not found"

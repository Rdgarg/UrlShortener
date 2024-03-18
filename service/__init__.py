from flask import Flask, request
from markupsafe import escape

from service.urlshortener import urlshortener, getActualUrl

# from urlshortener import urlshortener, getActualUrl

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/index')
def index_page():
    return 'Index page'


@app.route('/user/<username>')
def user_name(username):
    return f'User {escape(username)}'


@app.route('/shorten_url')
def shorten_url():
    url = request.args.get("url")
    return urlshortener(url)


@app.route('/actual_url')
def actual_url():
    url = request.args.get("url")
    return getActualUrl(url)

@app.route('/some')
def some():
    url = request.args.get("url")
    return urlshortener(url)


if __name__ == '__main__':
    app.run()

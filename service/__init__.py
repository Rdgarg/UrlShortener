from flask import Flask, request
from markupsafe import escape
from flask_mysqldb import MySQL
from service.UrlShortener import UrlShortener
from service.UrlDao import UrlDao

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'project'

mysql = MySQL(app)

urlDao = UrlDao(mysql)
urlShortener = UrlShortener(urlDao)

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
    return urlShortener.urlshortener(url)


@app.route('/actual_url')
def actual_url():
    url = request.args.get("url")
    return urlShortener.getActualUrl(url)

@app.route('/some')
def some():
    url = request.args.get("url")
    return urlShortener.urlshortener(url)


if __name__ == '__main__':
    app.run()

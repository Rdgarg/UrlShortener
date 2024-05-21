from flask import Flask, request
from markupsafe import escape
from flask_mysqldb import MySQL
from prometheus_client.utils import INF

from service.UrlShortener import UrlShortener
from service.UrlDao import UrlDao
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'project'

mysql = MySQL(app)

buckets = list(map(lambda x: x * 0.01, (.005, .01, .025, .05, .075, .1, .25, .5, .75, 1.0, 2.5, 5.0, 7.5, 10.0, INF)))

# buckets = (0.005, 0.1, 0.2, INF)

metrics = PrometheusMetrics(app, buckets=buckets)

print(metrics.buckets)

urlDao = UrlDao(mysql)
urlShortener = UrlShortener(urlDao)

by_path_counter = metrics.counter(
    'by_path_counter', 'Request count by request paths',
    labels={'path': lambda: request.path}
)

shorten_url_duration = metrics.histogram('shorten_url_duration', 'Duration of shorten_url call')
actual_url_duration = metrics.histogram('actual_url_duration', 'Duration of actual_url call')

shorten_url_summary = metrics.summary('shorten_url_summary', 'Summary of shorten_url')


@app.route('/')
@metrics.do_not_track()
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/index')
@metrics.do_not_track()
def index_page():
    return 'Index page'


@app.route('/user/<username>')
@metrics.do_not_track()
def user_name(username):
    return f'User {escape(username)}'


@app.route('/shorten_url')
@metrics.do_not_track()
@by_path_counter
@shorten_url_duration
def shorten_url():
    url = request.args.get("url")
    return urlShortener.urlshortener(url)


@app.route('/actual_url')
@metrics.do_not_track()
@by_path_counter
@actual_url_duration
def actual_url():
    url = request.args.get("url")
    return urlShortener.getActualUrl(url)


@app.route('/some')
@metrics.do_not_track()
def some():
    url = request.args.get("url")
    return urlShortener.urlshortener(url)


if __name__ == '__main__':
    app.run()

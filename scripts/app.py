from flask import Flask, request
from markupsafe import escape
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client.utils import INF
from flask_mysqldb import MySQL
import os
import validators

# from scripts.UrlDao import UrlDao
# from scripts.UrlShortener import UrlShortener
from UrlDao import UrlDao
from UrlShortener import UrlShortener

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
# app.config["MYSQL_DATABASE_USER"] = "root"
# app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("password")
# app.config["MYSQL_DATABASE_DB"] = os.getenv("db_name")
# app.config["MYSQL_DATABASE_HOST"] = os.getenv("MYSQL_SERVICE_HOST")
# app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("MYSQL_SERVICE_PORT"))
app.config['MYSQL_HOST'] = os.getenv("MYSQL_SERVICE_HOST")
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.getenv("password")
app.config['MYSQL_DB'] = os.getenv("db_name")
app.config['MYSQL_PORT'] = 3306
mysql.init_app(app)

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'project'
# app.config['MYSQL_PORT'] = 3306
# mysql.init_app(app)

buckets = list(map(lambda x: x * 0.01, (.005, .01, .025, .05, .075, .1, .25, .5, .75, 1.0, 2.5, 5.0, 7.5, 10.0, INF)))

# buckets = (0.005, 0.1, 0.2, INF)

metrics = PrometheusMetrics(app, buckets=buckets)

print(metrics.buckets)

print("running some shit")

urlDao = UrlDao(mysql)
urlShortener = UrlShortener(urlDao)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/index')
def index_page():
    return 'Index page'


@app.route('/shorten_url')
def shorten_url():
    url = request.args.get("url")
    return urlShortener.urlshortener(url)


@app.route('/actual_url')
def actual_url():
    url = request.args.get("url")
    return urlShortener.getActualUrl(url)

@app.route('/stats')
def stats():
    return urlShortener.get_stats()


if __name__ == '__main__':
    print("starting app scripts")
    app.run()

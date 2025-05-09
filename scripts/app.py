from flask import Flask, request, redirect, jsonify
from markupsafe import escape
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client.utils import INF
from flask_mysqldb import MySQL
import os
from redis import Redis
import logging
from google.cloud import logging as google_cloud_logging
from flask_cors import CORS

# from scripts.UrlDao import UrlDao
# from scripts.UrlShortener import UrlShortener
from UrlDao import UrlDao
from UrlShortener import UrlShortener

app = Flask(__name__)
redis = Redis(host='redis', port=6379)
CORS(app)

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

logging_client = google_cloud_logging.Client()
logging_client.setup_logging()  # Automatically configures handlers based on the environment

logger = logging.getLogger(__name__)


@app.route('/')
def hello_world():
    logger.info("This is home page")# put application's code here
    redis.incr("hits")
    return 'Hello World! I have been seen {} times.\n'.format(redis.get("hits").decode('utf-8'))


@app.route('/index')
def index_page():
    logger.info("This is index page")
    return 'Index page'


@app.route('/shorten_url')
def shorten_url():
    url = request.args.get("url")
    logger.info("This is shorten_url request, url is %s", url)
    short_url = urlShortener.urlshortener(url)
    return jsonify({"short_url": short_url})


@app.route('/actual_url')
def actual_url():
    url = request.args.get("url")
    logger.info("This is actual_url request, url is %s", url)
    original_url =  urlShortener.getActualUrl(url)
    return jsonify({"actual_url": original_url})

@app.route('/stats')
def stats():
    logger.info("This is a stats request")
    if request.args.get("url"):
        url = request.args.get("url")
        logger.info("This is a stats request with url %s", url)
        stats_for_url = urlShortener.get_stats_for_single_url(url)
        return stats_for_url
    else :
        logger.info("This is a stats request without url")
        return urlShortener.get_stats()


@app.route('/sendme')
def sendme():
    url = request.args.get("url")
    logger.info("This is a sendme request with url %s", url)
    original_url = urlShortener.getActualUrl(url)
    return redirect(original_url, 302)


if __name__ == '__main__':
    logger.info("starting app scripts")
    app.run()

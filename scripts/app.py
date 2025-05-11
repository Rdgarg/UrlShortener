from flask import Flask, request, redirect, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client.utils import INF
from flask_mysqldb import MySQL
import os
from redis import Redis
import logging
from google.cloud import logging as google_cloud_logging
from flask_cors import CORS
from google.oauth2 import id_token
from google.auth.transport import requests as grequests

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

CLIENT_ID = '251182287536-srbj0sbra4rtlh0prd5j7qobgd7u4frs.apps.googleusercontent.com'

@app.route('/')
def hello_world():
    logger.info("This is home page")# put application's code here
    redis.incr("hits")
    return 'Hello World! I have been seen {} times.\n'.format(redis.get("hits").decode('utf-8'))

@app.route('/login', methods=['POST'])
def login():
    logger.info("Login request")
    token = request.json.get('token')
    try:
        # Verify the token using Google's library
        idinfo = id_token.verify_oauth2_token(token, grequests.Request(), CLIENT_ID)

        # ID token is valid. Get user info.
        user_id = idinfo['sub']
        email = idinfo.get('email')
        name = idinfo.get('name')
        urlShortener.add_user_info(user_id, email, name)
        redis.set(user_id, "true")
        # You can now use this info in your app
        return jsonify({"message": "Login successful", "email": email, "name": name})

    except ValueError:
        # Invalid token
        return jsonify({"error": "Invalid token"}), 400
@app.route('/index')
def index_page():
    logger.info("This is index page")
    return 'Index page'


@app.route('/shorten_url')
def shorten_url():
    user_id = validate_token(request)
    if user_id is None:
        return jsonify({"error": "Unauthorized"}), 401

    url = request.args.get("url")
    logger.info("This is shorten_url request, url is %s", url)
    short_url = urlShortener.urlshortener(url, user_id)
    return jsonify({"short_url": short_url})


@app.route('/actual_url')
def actual_url():
    if validate_token(request) is None:
        return jsonify({"error": "Unauthorized"}), 401
    url = request.args.get("url")
    logger.info("This is actual_url request, url is %s", url)
    original_url =  urlShortener.getActualUrl(url)
    return jsonify({"actual_url": original_url})

@app.route('/stats')
def stats():
    if validate_token(request) is None:
        return jsonify({"error": "Unauthorized"}), 401
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
    if validate_token(request) is None:
        return jsonify({"error": "Unauthorized"}), 401
    url = request.args.get("url")
    logger.info("This is a sendme request with url %s", url)
    original_url = urlShortener.getActualUrl(url)
    return redirect(original_url, 302)

def validate_token(request):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None

    token = auth_header.split(' ')[1]
    try:
        idinfo = id_token.verify_oauth2_token(token, grequests.Request(), CLIENT_ID)
    except ValueError:
        logger.error("Invalid token")
        return None
    user_id = idinfo['sub']
    if redis.get(user_id) is None:
        logger.error("User not found in Redis")
        return None
    return user_id


if __name__ == '__main__':
    logger.info("starting app scripts")
    app.run()

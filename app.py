from flask import Flask
from markupsafe import escape

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

if __name__ == '__main__':
    app.run()

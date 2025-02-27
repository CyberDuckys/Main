from flask import Flask
from website.views import views
from flask_mysqldb import MySQL

mysql = MySQL()

def create_app():
    app = Flask(__name__)

    mysql.init_app(app)
    app.register_blueprint(views, url_prefix='/')

    return app
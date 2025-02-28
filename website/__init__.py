from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
from website.views import Views

# Laad de omgevingsvariabelen
load_dotenv()

# Initialiseer MySQL
mysql = MySQL()

def create_app():
    app = Flask(__name__)

    # Database configuratie via .env
    app.config['MYSQL_HOST'] = os.getenv('DB_HOST')
    app.config['MYSQL_USER'] = os.getenv('DB_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv('DB_NAME')

    mysql.init_app(app)

    # Registreer de blueprint correct
    views = Views(mysql)
    app.register_blueprint(views.views, url_prefix='/')

    return app
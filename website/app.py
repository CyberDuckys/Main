from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from views import create_views
import config
import os

# Laad de omgevingsvariabelen
load_dotenv()

# Initialiseer MySQL
mysql = MySQL()

def create_app():
    app = Flask(__name__)

    # Database configuratie via omgevingsvariabelen
    app.config['MYSQL_HOST'] = os.getenv('DB_HOST')
    app.config['MYSQL_USER'] = os.getenv('DB_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv('DB_NAME')

    mysql.init_app(app)

    # Importeer en registreer Blueprints
    views = create_views(mysql)  # Geeft MySQL-verbinding door aan views.py
    app.register_blueprint(views, url_prefix='/')



    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)
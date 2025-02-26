from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from views import Views  # Import the Views class instead of create_views
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

    # Gebruik de Views klasse om de blueprint te maken en te registreren
    views = Views(mysql)  # Geeft de MySQL-verbinding door aan de Views klasse
    app.register_blueprint(views.views, url_prefix='/')  # Registreer de blueprint

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)
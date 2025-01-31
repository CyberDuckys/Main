from flask import Flask
from flask_mysqldb import MySQL
import config

# Initialize MySQL object globally
mysql = MySQL()

def create_app():
    app = Flask(__name__)
    from .views import views
    app.register_blueprint(views, url_prefix='/')
    
    # MySQL configuration
    app.config['MYSQL_HOST'] = config.db_host
    app.config['MYSQL_USER'] = config.db_user
    app.config['MYSQL_PASSWORD'] = config.db_password
    app.config['MYSQL_DB'] = config.db_db


    # Initialize MySQL with app
    mysql.init_app(app)

    return app

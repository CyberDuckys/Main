from flask import Flask
from flask_mysqldb import MySQL

# Initialize MySQL object globally
mysql = MySQL()

def create_app():
    app = Flask(__name__)

    from .views import views
    app.register_blueprint(views, url_prefix='/')
    
    # MySQL configuration
    app.config['MYSQL_HOST'] = 'mysql.atd.avans.nl'
    app.config['MYSQL_USER'] = 's2233725'
    app.config['MYSQL_PASSWORD'] = 'ab12345'
    app.config['MYSQL_DB'] = 's2233725'


    # Initialize MySQL with app
    mysql.init_app(app)

    return app

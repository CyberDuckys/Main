import os
import pytest
from dotenv import load_dotenv
import mysql.connector
from website import create_app

# Laad de .env-variabelen
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'website', '.env')
load_dotenv(dotenv_path)

@pytest.fixture(scope='session')
def app():
    """Initialiseer de Flask-app voor testing"""
    app = create_app()
    return app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()

@pytest.fixture(scope='session')
def db_connection():
    """Maakt een echte verbinding met de database"""
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    yield connection
    connection.close()
    
@pytest.fixture
def db_cursor(db_connection):
    """Geeft een cursor voor de database"""
    cursor = db_connection.cursor()
    yield cursor
    cursor.close()
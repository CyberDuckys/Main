from flask import Blueprint, render_template
from . import mysql  # Import the globally initialized `mysql`
views = Blueprint('views', __name__)

#send query to database and return output
def database(query):
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

@views.route('/')
def index():
    result = database("select magazijn.product_id, magazijn.voorraad_aantal, products.naam from magazijn INNER JOIN products ON magazijn.product_id=products.product_id;")
    product1 = result[0]
    print(product1, flush=True)
    return render_template("index.html", products=result)

@views.route('/klanten')
def klanten():
    return render_template("klanten.html")

@views.route('/koeriers')
def koeriers():
    return render_template("koeriers.html")

@views.route('/inkoop')
def inkoop():
    return render_template("inkoop.html")

@views.route('/voorraad')
def voorraad():
    return render_template("voorraad.html")

@views.route('/bestelgeschiedenis')
def bestelgeschiedenis():
    return render_template("bestelgeschiedenis.html")

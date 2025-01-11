from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template("index.html")

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
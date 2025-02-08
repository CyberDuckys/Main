from flask import Blueprint, redirect, render_template, request, url_for
from . import mysql  # Import the globally initialized mysql
from datetime import datetime
from .static.backend.general_backend import database

views = Blueprint('views', __name__)

klanten = (
    (1, 'Aalbert Hain', 'dhr amir aalbert hain', 'http://ah.nl', '+31 12345678'),
    (2, 'JANTJE Hain', 'dhr JANTJE aalbert hain', 'http://jumbo.nl', '+31 12345678'),
)

financien_data = (
    (1, 'Factuur 1', 100.00, 'Betaald', '2023-03-02'),
    (2, 'Factuur 2', 200.00, 'Betaald', '2023-03-02'),
    (3, 'Factuur 3', 300.00, 'Betaald', '2023-03-02'),
    (4, 'Factuur 4', 400.00, 'Betaald', '2023-03-02')
)

# Dashboard Route
@views.route('/')
def index():
    bijnaOpProducten = database("select * from s2233725.products")
    if bijnaOpProducten is None:
        bijnaOpProducten = (
            (1, "banaan", 10),
            (2, "appel", 5),
            (3, "peer", 8)
        )
    print(bijnaOpProducten)
    return render_template("index.html", bijnaOpProducten=bijnaOpProducten)

# Klanten Route
@views.route('/klanten')
def klantenlijst():
    return render_template("klanten.html", klanten=klanten)

# Financiële Routes
@views.route('/financien/<int:klant_id>')
def financien(klant_id):
    klant_financien = financien_data[klant_id - 1]
    klant = next((k for k in klanten if k[0] == klant_id), None)
    
    if klant is None:
        return "Klant niet gevonden", 404

    return render_template("financien.html", klant_id=klant_id, finance=klant_financien)

@views.route('/financien/toevoegen', methods=['GET', 'POST'])
def financien_toevoegen():
    if request.method == 'POST':
        klant = request.form.get('klant')
        bedrag = request.form.get('bedrag')
        datum = request.form.get('datum')
        status = request.form.get('status')

        if not klant.isdigit():
            return "Ongeldig klant ID. Zorg ervoor dat je een geldig nummer invoert.", 400

        klant_id = int(klant)
        nieuwe_finance = {
            "id": len(financien_data.get(klant_id, [])) + 1,
            "beschrijving": f"Nieuwe factuur voor klant {klant_id}",
            "bedrag": bedrag,
            "datum": datum,
            "status": status
        }

        if klant_id in financien_data:
            financien_data[klant_id].append(nieuwe_finance)
        else:
            financien_data[klant_id] = [nieuwe_finance]

        return redirect(url_for('views.financien', klant_id=klant_id))
    
    return render_template("financien_toevoegen.html")

# Voorraad Route
@views.route('/voorraad')
def voorraad():
    voorraad = database("select * from products;")
    if voorraad is None:
        voorraad = (
            (1, "banaan", 1, "koeling", "A12", "5", "2025-02-09"),
            (2, "appel", 1, "koeling", "A13", "10", "2025-02-10"),
            (3, "peer", 1, "koeling", "A14", "8", "2025-02-11")
        )
    return render_template("voorraad.html", voorraad=voorraad)

@views.route('/voorraadProductToevoegen', methods=['GET', 'POST'])
def voorraadProductToevoegen():
    if request.method == 'POST':
        new_product = (
            int(request.form['id']),
            request.form['product'],
            int(request.form['batchnumber']),
            request.form['storageadvice'],
            request.form['location'],
            int(request.form['amount']),
            datetime.now().strftime("%Y-%m-%d")
        )
        database(
            f"INSERT INTO products (product_id, product, batchnummer, bewaaradvies, locatie, aantal, houdbaarheid) "
            f"VALUES ('{new_product[0]}','{new_product[1]}','{new_product[2]}','{new_product[3]}','{new_product[4]}','{new_product[5]}','{new_product[6]}')"
        )
        return redirect(url_for('views.voorraad'))
    
    return render_template('voorraadProductToevoegen.html')

# Overige Routes
@views.route('/koeriers')
def koeriers():
    return render_template("koeriers.html")

@views.route('/verkoop')
def verkoop():
    return render_template("verkoop.html")

@views.route('/inkoop')
def inkoop():
    return render_template("inkoop.html")

@views.route('/bestelgeschiedenis')
def bestelgeschiedenis():
    return render_template("bestelgeschiedenis.html")

@views.route('/koeriers/klant-info/<int:klant_id>')
def koeriers_klant_info(klant_id):
    klant = klanten[klant_id]
    koerier_info = {
        "track": f"Trace {klant_id}123",
        "levermoment": "9:00 - 12:00",
        "adres": "Example Street, 1234 AB Example"
    }
    
    if klant is None:
        return "Klant niet gevonden", 404
    
    return render_template("koeriers_klant_info.html", klant=klant, koerier_info=koerier_info)
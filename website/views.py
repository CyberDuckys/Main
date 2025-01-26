from flask import Blueprint, redirect, render_template, request, url_for
from . import mysql  # Import the globally initialized `mysql`
from datetime import datetime
from .static.backend.general_backend import database
views = Blueprint('views', __name__)

# Dummy data
# klanten = [
#     {'id': 1, 'naam': 'Aalbert Hain', 'contact': 'Dhr Amir Aalbert Hain', 'website': 'http://ah.nl', 'telefoon': '+31 12345678'},
#     {'id': 2, 'naam': 'Bumbo', 'contact': 'Mevr Bell Bumbo', 'website': 'http://bumbo.com', 'telefoon': '+31 12345678'},
#     {'id': 3, 'naam': 'Cidl', 'contact': 'Dhr Christoph Cidl', 'website': 'http://cidl.net', 'telefoon': '+31 12345678'},
# ]

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


@views.route('/')
def index():
    # Volgorde: ID, Product, Voorraad
    # bijnaOpProducten = database("select magazijn.product_id, magazijn.voorraad_aantal, products.naam from magazijn INNER JOIN products ON magazijn.product_id=products.product_id;")
    bijnaOpProducten = ((1,2,"banaan"),(1,2,"banaan"),(1,2,"banaan"))
    time = datetime.now().strftime("%H:%M")
    date = datetime.now().strftime("%d-%m-%Y")
    day = datetime.now().strftime("%A")
    return render_template("index.html", bijnaOpProducten=bijnaOpProducten, time=time, date=date, day=day)

@views.route('/klanten')
def klantenlijst():
    # Volgorde: ID, Naam, Contact, Website, Telefoon
    # klanten = database("select magazijn.product_id, magazijn.voorraad_aantal, products.naam from magazijn INNER JOIN products ON magazijn.product_id=products.product_id;"))
    # klanten = [
    #     {'id': 1, 'naam': 'Aalbert Hain', 'contact': 'Dhr Amir Aalbert Hain', 'website': 'http://ah.nl', 'telefoon': '+31 12345678'},
    #     {'id': 2, 'naam': 'Bumbo', 'contact': 'Mevr Bell Bumbo', 'website': 'http://bumbo.com', 'telefoon': '+31 12345678'},
    #     {'id': 3, 'naam': 'Cidl', 'contact': 'Dhr Christoph Cidl', 'website': 'http://cidl.net', 'telefoon': '+31 12345678'},
    # ]
    klanten = (
        (1, 'Aalbert Hain', 'dhr amir aalbert hain', 'http://ah.nl', '+31 12345678'),
        (2, 'JANTJE Hain', 'dhr JANTJE aalbert hain', 'http://jumbo.nl', '+31 12345678'),
    )
    return render_template("klanten.html", klanten=klanten)


@views.route('/financien/<int:klant_id>')
def financien(klant_id):
    # Haal klantfinanciën op
    klant_financien = financien_data[klant_id - 1]
    print(klant_financien)
    # Zoek de klantnaam
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

@views.route('/financien/wijzigen/<int:finance_id>', methods=['GET', 'POST'])
def financien_wijzigen_finance(finance_id):
    for klant_id, financien in financien_data.items():
        for finance in financien:
            if finance['id'] == finance_id:
                geselecteerde_finance = finance
                break
        else:
            continue
        break
    else:
        return "Financiële record niet gevonden", 404

    if request.method == 'POST':
        geselecteerde_finance['beschrijving'] = request.form.get('beschrijving')
        geselecteerde_finance['bedrag'] = request.form.get('bedrag')
        geselecteerde_finance['status'] = request.form.get('status')
        geselecteerde_finance['datum'] = request.form.get('datum')

        return redirect(url_for('views.financien', klant_id=klant_id))

    return render_template("financien_wijzigen.html", financien=geselecteerde_finance)

@views.route('/financien/wijzigen/klant/<int:klant_id>', methods=['GET', 'POST'])
def financien_wijzigen_klant(klant_id):
    klant_financien = financien_data[klant_id]
    if request.method == 'POST':
        financien = (
                    klant_id,            #id
                    request.form['beschrijving'],            #product
                    request.form['bedrag'],   #batchnummer
                    request.form['status'],      #storageadvice
                    datetime.now().strftime("%Y-%m-%d") #date
                )
        database(f"UPDATE klanten set description = '{financien[1]}', amount = '{financien[2]}', status = '{financien[3]}'")
        return redirect(url_for('views.klanten'))
    return render_template("financien_wijzigen.html", klant_id=klant_id, financien=klant_financien)


@views.route('/koeriers')
def koeriers():
    return render_template("koeriers.html")

@views.route('/inkoop')
def inkoop():
    return render_template("inkoop.html")

@views.route('/voorraad')
def voorraad():
    voorraad = database("select * from products;")
    return render_template("voorraad.html", voorraad=voorraad)

@views.route('/bestelgeschiedenis')
def bestelgeschiedenis():
    return render_template("bestelgeschiedenis.html")

# Route voor de product toevoeg-pagina
@views.route('/voorraadProductToevoegen', methods=['GET', 'POST'])
def voorraadProductToevoegen():    
    if request.method == 'POST':
        # Nieuwe data ophalen uit het formulier
        new_product = (
            int(request.form['id']),            #id
            request.form['product'],            #product
            int(request.form['batchnumber']),   #batchnummer
            request.form['storageadvice'],      #storageadvice
            request.form['location'],           #location
            int(request.form['amount']),        #amount
            datetime.now().strftime("%Y-%m-%d") #date
        )
        database(f"INSERT INTO products (product_id, product, batchnummer, bewaaradvies, locatie, aantal, houdbaarheid) VALUES ('{new_product[0]}','{new_product[1]}','{new_product[2]}','{new_product[3]}','{new_product[4]}','{new_product[5]}','{new_product[6]}')")
        return redirect(url_for('views.voorraad'))  # Terug naar de voorraad.html
    return render_template('voorraadProductToevoegen.html')

@views.route('/koeriers/klant-info/<int:klant_id>')
def koeriers_klant_info(klant_id):
    # Retrieve klant and koerier info
    klant = next((k for k in klanten if k['id'] == klant_id), None)
    koerier_info = {
        "track": f"Trace {klant_id}123",
        "levermoment": "9:00 - 12:00",
        "adres": "Example Street, 1234 AB Example"
    }

    if klant is None:
        return "Klant niet gevonden", 404

    return render_template("koeriers_klant_info.html", klant=klant, koerier_info=koerier_info)
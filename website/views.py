from flask import Blueprint, redirect, render_template, request, url_for

views = Blueprint('views', __name__)

# Dummy data
klanten = [
    {'id': 1, 'naam': 'Aalbert Hain', 'contact': 'Dhr Amir Aalbert Hain', 'website': 'http://ah.nl', 'telefoon': '+31 12345678'},
    {'id': 2, 'naam': 'Bumbo', 'contact': 'Mevr Bell Bumbo', 'website': 'http://bumbo.com', 'telefoon': '+31 12345678'},
    {'id': 3, 'naam': 'Cidl', 'contact': 'Dhr Christoph Cidl', 'website': 'http://cidl.net', 'telefoon': '+31 12345678'},
]

financien_data = {
    1: [
        {'id': 1, 'beschrijving': 'Factuur 1', 'bedrag': '€100,00', 'status': 'Onbetaald', 'datum': '01-01-2023'},
        {'id': 2, 'beschrijving': 'Factuur 2', 'bedrag': '€200,00', 'status': 'Betaald', 'datum': '15-01-2023'},
    ],
    2: [
        {'id': 3, 'beschrijving': 'Factuur 3', 'bedrag': '€150,00', 'status': 'Onbetaald', 'datum': '20-02-2023'},
    ],
    3: [
        {'id': 4, 'beschrijving': 'Factuur 4', 'bedrag': '€300,00', 'status': 'Betaald', 'datum': '05-03-2023'},
    ],
}

@views.route('/')
def index():
    return render_template("index.html")

@views.route('/klanten')
def klantenlijst():
    klanten = [
        {'id': 1, 'naam': 'Aalbert Hain', 'contact': 'Dhr Amir Aalbert Hain', 'website': 'http://ah.nl', 'telefoon': '+31 12345678'},
        {'id': 2, 'naam': 'Bumbo', 'contact': 'Mevr Bell Bumbo', 'website': 'http://bumbo.com', 'telefoon': '+31 12345678'},
        {'id': 3, 'naam': 'Cidl', 'contact': 'Dhr Christoph Cidl', 'website': 'http://cidl.net', 'telefoon': '+31 12345678'},
    ]
    return render_template("klanten.html", klanten=klanten)


@views.route('/financien/<int:klant_id>')
def financien(klant_id):
    # Haal klantfinanciën op
    klant_financien = financien_data.get(klant_id, [])
    
    # Zoek de klantnaam
    klant = next((k for k in klanten if k['id'] == klant_id), None)
    
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
    klant_financien = financien_data.get(klant_id, [])

    if request.method == 'POST':
        for finance in klant_financien:
            if str(finance['id']) == request.form.get('id'):
                finance['beschrijving'] = request.form.get('beschrijving')
                finance['bedrag'] = request.form.get('bedrag')
                finance['datum'] = request.form.get('datum')
                finance['status'] = request.form.get('status')
                break

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
    return render_template("voorraad.html")

@views.route('/bestelgeschiedenis')
def bestelgeschiedenis():
    return render_template("bestelgeschiedenis.html")


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

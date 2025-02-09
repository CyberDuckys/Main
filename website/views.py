from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from datetime import datetime

def create_views(mysql):
    views = Blueprint('views', __name__)

    def execute_query(query, params=None):
        """ Voert een databasequery uit en retourneert het resultaat. """
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute(query, params or ())

        if query.strip().lower().startswith("select"):
            result = cursor.fetchall()
        else:
            conn.commit()
            result = None

        cursor.close()
        return result

    # 📌 DASHBOARD
    @views.route('/')
    def index():
        bijna_op_producten = execute_query("""
            SELECT p.naam, v.expiratiedatum, v.aantal
            FROM voorraad v
            JOIN products p ON v.product_id = p.product_id
            JOIN magazijn m ON v.magazijn_id = m.magazijn_id
            WHERE v.aantal <= 200
        """) or []

        print(bijna_op_producten)  # Debug output in de terminal
        return render_template("index.html", bijnaOpProducten=bijna_op_producten)
    
      # 📌 CO₂ TRACKER API
    @views.route('/api/co2-data')
    def co2_data():
        try:
            totaal_km = execute_query("SELECT SUM(km) FROM bestellingen")[0][0] or 0
            urgent_km = execute_query("SELECT SUM(km) FROM bestellingen WHERE spoed = 1")[0][0] or 0

            # Zet Decimal om naar float
            totaal_km = float(totaal_km)
            urgent_km = float(urgent_km)

            totaal_co2 = round(totaal_km * 0.008, 2)
            urgent_co2 = round(urgent_km * 0.008, 2)

            return jsonify({
                "totaal_km": totaal_km,
                "totaal_co2": totaal_co2,
                "urgent_km": urgent_km,
                "urgent_co2": urgent_co2
            })

        except Exception as e:
            return jsonify({"error": "Interne serverfout", "details": str(e)}), 500

    # 📌 KLANTEN
    @views.route('/klanten')
    def klantenlijst():
        klanten = execute_query("SELECT klant_id, naam, adres, telefoonnummer, jaaromzet FROM klant")
        return render_template("klanten.html", klanten=klanten)

    # 📌 FINANCIËN
    @views.route('/financien/<int:klant_id>')
    def financien(klant_id):
        klant = execute_query("SELECT * FROM klant WHERE klant_id = %s", (klant_id,))
        klant_financien = execute_query("SELECT * FROM administratie WHERE klant_id = %s", (klant_id,))

        if not klant:
            return "Klant niet gevonden", 404

        return render_template("financien.html", klant=klant, finance=klant_financien)

    @views.route('/financien/toevoegen', methods=['GET', 'POST'])
    def financien_toevoegen():
        if request.method == 'POST':
            klant_id = request.form.get('klant')
            bedrag = request.form.get('bedrag')
            datum = request.form.get('datum')
            status = request.form.get('status')

            if not klant_id.isdigit():
                return "Ongeldig klant ID.", 400

            execute_query("""
                INSERT INTO administratie (klant_id, factuur_id, betaalstatus, datum) 
                VALUES (%s, %s, %s, %s)
            """, (klant_id, bedrag, status, datum))

            return redirect(url_for('views.financien', klant_id=klant_id))

        klanten = execute_query("SELECT klant_id, naam FROM klant")
        return render_template("financien_toevoegen.html", klanten=klanten)

    # 📌 VOORRAAD
    @views.route('/voorraad')
    def voorraad():
        voorraad_data = execute_query("""
            SELECT v.voorraad_id, p.naam, v.batchnummer, v.expiratiedatum, v.aantal, v.minimale_voorraad, m.locatie 
            FROM voorraad v
            JOIN products p ON v.product_id = p.product_id
            JOIN magazijn m ON v.magazijn_id = m.magazijn_id
        """)
        return render_template("voorraad.html", voorraad=voorraad_data)

    @views.route('/voorraadProductToevoegen', methods=['GET', 'POST'])
    def voorraadProductToevoegen():
        if request.method == 'POST':
            product_id = request.form['product']
            batchnummer = request.form['batchnumber']
            locatie = request.form['location']
            aantal = request.form['amount']
            houdbaarheid = datetime.now().strftime("%Y-%m-%d")

            execute_query("""
                INSERT INTO voorraad (product_id, batchnummer, locatie, aantal, expiratiedatum) 
                VALUES (%s, %s, %s, %s, %s)
            """, (product_id, batchnummer, locatie, aantal, houdbaarheid))

            return redirect(url_for('views.voorraad'))

        producten = execute_query("SELECT product_id, naam FROM products")
        return render_template('voorraadProductToevoegen.html', producten=producten)

    # 📌 VERKOOP
    @views.route('/verkoop')
    def verkoop():
        verkoop_data = execute_query("""
            SELECT v.verkoop_id, k.naam, b.bestelling_id, v.datum, v.totaal_bedrag, v.betaalstatus 
            FROM verkoop v
            JOIN bestellingen b ON v.bestelling_id = b.bestelling_id
            JOIN klant k ON v.klant_id = k.klant_id
        """)
        return render_template("verkoop.html", verkoop=verkoop_data)

    # 📌 INKOOP
    @views.route('/inkoop')
    def inkoop():
        inkoop_data = execute_query("""
            SELECT i.inkoop_id, p.naam, i.aantal, i.bestel_datum, i.prijs_per_eenheid, i.leverancier 
            FROM inkoop i
            JOIN products p ON i.product_id = p.product_id
        """)
        return render_template("inkoop.html", inkoop=inkoop_data)

    # 📌 BESTELGESCHIEDENIS
    @views.route('/bestelgeschiedenis')
    def bestelgeschiedenis():
        bestellingen = execute_query("""
            SELECT i.inkoop_id, p.naam, i.leverancier, i.prijs_per_eenheid, i.bestel_datum
            FROM inkoop i
            JOIN products p ON i.product_id = p.product_id
        """)
        return render_template("bestelgeschiedenis.html", bestellingen=bestellingen)

    # 📌 KOERIERS
    @views.route('/koeriers')
    def koeriers():
        koeriers_data = execute_query("SELECT koerier_id, naam, telefoonnummer, regio FROM koeriers")
        leveringen = execute_query("""
            SELECT b.bestelling_id, b.datum, k.naam, k.adres, c.naam 
            FROM bestellingen b
            JOIN klant k ON b.klant_id = k.klant_id
            JOIN koeriers c ON b.koerier_id = c.koerier_id
        """)
        return render_template("koeriers.html", koeriers=koeriers_data, leveringen=leveringen)

    @views.route('/koeriers/klant-info/<int:klant_id>')
    def koeriers_klant_info(klant_id):
        klant = execute_query("SELECT * FROM klant WHERE klant_id = %s", (klant_id,))
        koerier_info = execute_query("SELECT * FROM koeriers WHERE koerier_id = %s", (klant_id,))

        if not klant:
            return "Klant niet gevonden", 404

        return render_template("koeriers_klant_info.html", klant=klant, koerier_info=koerier_info)

    return views  # ✅ Blueprint teruggeven
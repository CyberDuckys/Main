from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from datetime import datetime

class Views:
    def __init__(self, mysql):
        self.mysql = mysql
        self.views = Blueprint('views', __name__)

        self._register_routes()

    def _execute_query(self, query, params=None):
        """ Voert een databasequery uit en retourneert het resultaat. """
        conn = self.mysql.connection
        cursor = conn.cursor()
        cursor.execute(query, params or ())

        if query.strip().lower().startswith("select"):
            result = cursor.fetchall()
        else:
            conn.commit()
            result = None

        cursor.close()
        return result

    def _register_routes(self):
        """Registreer de routes voor de Flask Blueprint"""
        self.views.add_url_rule('/', view_func=self.index)
        self.views.add_url_rule('/api/co2-data', view_func=self.co2_data)
        self.views.add_url_rule('/klanten', view_func=self.klantenlijst)
        self.views.add_url_rule('/financien/<int:klant_id>', view_func=self.financien)
        self.views.add_url_rule('/financien/toevoegen', methods=['GET', 'POST'], view_func=self.financien_toevoegen)
        self.views.add_url_rule('/voorraad', view_func=self.voorraad)
        self.views.add_url_rule('/voorraadProductToevoegen', methods=['GET', 'POST'], view_func=self.voorraadProductToevoegen)
        self.views.add_url_rule('/voorraadToevoegen', methods=['GET', 'POST'], view_func=self.voorraadToevoegen)
        self.views.add_url_rule('/verkoop', view_func=self.verkoop)
        self.views.add_url_rule('/inkoop', view_func=self.inkoop)
        self.views.add_url_rule('/bestelgeschiedenis', view_func=self.bestelgeschiedenis)
        self.views.add_url_rule('/koeriers', view_func=self.koeriers)
        self.views.add_url_rule('/koeriers/klant-info/<int:klant_id>', view_func=self.koeriers_klant_info)

    # 📌 DASHBOARD
    def index(self):
        bijna_op_producten = self._execute_query("""
            SELECT p.naam, v.toegevoegd_op, v.aantal
            FROM voorraad v
            JOIN products p ON v.product_id = p.product_id
            JOIN magazijn m ON v.magazijn_id = m.magazijn_id
            WHERE v.aantal <= 200
            ORDER BY v.aantal
        """) or []

        print(bijna_op_producten)  # Debug output in de terminal
        return render_template("index.html", bijnaOpProducten=bijna_op_producten)
    
    # 📌 CO₂ TRACKER API
    def co2_data(self):
        try:
            totaal_km = self._execute_query("SELECT SUM(km) FROM bestellingen")[0][0] or 0
            urgent_km = self._execute_query("SELECT SUM(km) FROM bestellingen WHERE spoed = 1")[0][0] or 0

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
    def klantenlijst(self):
        klanten = self._execute_query("SELECT klant_id, naam, adres, telefoonnummer, jaaromzet FROM klant")
        return render_template("klanten.html", klanten=klanten)

    # 📌 FINANCIËN
    def financien(self, klant_id):
        klant = self._execute_query("SELECT * FROM klant WHERE klant_id = %s", (klant_id,))
        klant_financien = self._execute_query("SELECT * FROM administratie WHERE klant_id = %s", (klant_id,))

        if not klant:
            return "Klant niet gevonden", 404

        return render_template("financien.html", klant=klant, finance=klant_financien)

    def financien_toevoegen(self):
        if request.method == 'POST':
            klant_id = request.form.get('klant')
            bedrag = request.form.get('bedrag')
            datum = request.form.get('datum')
            status = request.form.get('status')

            if not klant_id.isdigit():
                return "Ongeldig klant ID.", 400

            self._execute_query("""
                INSERT INTO administratie (klant_id, factuur_id, betaalstatus, datum) 
                VALUES (%s, %s, %s, %s)
            """, (klant_id, bedrag, status, datum))

            return redirect(url_for('views.financien', klant_id=klant_id))

        klanten = self._execute_query("SELECT klant_id, naam FROM klant")
        return render_template("financien_toevoegen.html", klanten=klanten)

    # 📌 VOORRAAD
    def voorraad(self):
        voorraad_data = self._execute_query("""
            SELECT v.voorraad_id, p.naam, v.batchnummer, v.toegevoegd_op, v.aantal, m.locatie 
            FROM voorraad v
            JOIN products p ON v.product_id = p.product_id
            JOIN magazijn m ON v.magazijn_id = m.magazijn_id
            ORDER BY v.voorraad_id ASC, m.locatie DESC
        """)
        return render_template("voorraad.html", voorraad=voorraad_data)

    def voorraadProductToevoegen(self):
        if request.method == 'POST':
            product_id = request.form['product']
            batchnummer = request.form['batchnumber']
            locatie = request.form['location']
            aantal = request.form['amount']
            houdbaarheid = datetime.now().strftime("%Y-%m-%d")

            self._execute_query("""
                INSERT INTO voorraad (product_id, batchnummer, locatie, aantal, expiratiedatum) 
                VALUES (%s, %s, %s, %s, %s)
            """, (product_id, batchnummer, locatie, aantal, houdbaarheid))

            return redirect(url_for('views.voorraad'))

        producten = self._execute_query("SELECT product_id, naam FROM products")
        return render_template('voorraadProductToevoegen.html', producten=producten)

    def voorraadToevoegen(self):
        producten = self._execute_query("""
            SELECT product_id, naam FROM products
            ORDER BY product_id;""")
        
        locaties = self._execute_query("""
            SELECT magazijn_id, locatie FROM magazijn
            ORDER BY locatie;""")
        
        if request.method == 'POST':
            locatie = request.form['location']
            product_id = request.form['product']
            batchnummer = request.form['batchnumber']
            aantal = request.form['amount']
            toegevoegd_op = datetime.now().strftime("%Y-%m-%d")

            self._execute_query("""
                INSERT INTO voorraad (magazijn_id, product_id, batchnummer, toegevoegd_op, aantal ) 
                VALUES (%s, %s, %s, %s, %s)
            """, (locatie, product_id, batchnummer, toegevoegd_op, aantal))

            return redirect(url_for('views.voorraad'))

        return render_template('voorraadToevoegen.html', producten=producten, locaties=locaties)

    # 📌 VERKOOP
    def verkoop(self):
        verkoop_data = self._execute_query("""
            SELECT v.verkoop_id, k.naam, b.bestelling_id, v.datum, v.totaal_bedrag, v.betaalstatus 
            FROM verkoop v
            JOIN bestellingen b ON v.bestelling_id = b.bestelling_id
            JOIN klant k ON v.klant_id = k.klant_id
            ORDER BY v.verkoop_id
        """)
        return render_template("verkoop.html", verkoop=verkoop_data)

    # 📌 INKOOP
    def inkoop(self):
        inkoop_data = self._execute_query("""
            SELECT i.inkoop_id, p.naam, i.aantal, i.bestel_datum, i.prijs_per_eenheid, i.leverancier 
            FROM inkoop i
            JOIN products p ON i.product_id = p.product_id
            ORDER BY i.inkoop_id
        """)
        return render_template("inkoop.html", inkoop=inkoop_data)

    # 📌 BESTELGESCHIEDENIS
    def bestelgeschiedenis(self):
        bestellingen = self._execute_query("""
            SELECT i.inkoop_id, p.naam, i.leverancier, i.prijs_per_eenheid, i.bestel_datum
            FROM inkoop i
            JOIN products p ON i.product_id = p.product_id
        """)
        return render_template("bestelgeschiedenis.html", bestellingen=bestellingen)

    # 📌 KOERIERS
    def koeriers(self):
        koeriers_data = self._execute_query("SELECT koerier_id, naam, telefoonnummer, regio FROM koeriers")
        leveringen = self._execute_query("""
            SELECT b.bestelling_id, b.datum, k.naam, k.adres, c.naam 
            FROM bestellingen b
            JOIN klant k ON b.klant_id = k.klant_id
            JOIN koeriers c ON b.koerier_id = c.koerier_id
            ORDER BY b.bestelling_id
        """)
        return render_template("koeriers.html", koeriers=koeriers_data, leveringen=leveringen)

    def koeriers_klant_info(self, klant_id):
        klant = self._execute_query("SELECT * FROM klant WHERE klant_id = %s", (klant_id,))
        koerier_info = self._execute_query("SELECT * FROM koeriers WHERE koerier_id = %s", (klant_id,))

        if not klant:
            return "Klant niet gevonden", 404

        return render_template("koeriers_klant_info.html", klant=klant, koerier_info=koerier_info)
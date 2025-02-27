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
        self.views.add_url_rule('/financien/wijzigen/<int:financien_id>', methods=['GET', 'POST'], view_func=self.financien_wijzigen)
        self.views.add_url_rule('/voorraad', view_func=self.voorraad)
        self.views.add_url_rule('/voorraadProductToevoegen', methods=['GET', 'POST'], view_func=self.voorraadProductToevoegen)
        self.views.add_url_rule('/voorraadToevoegen', methods=['GET', 'POST'], view_func=self.voorraadToevoegen)
        self.views.add_url_rule('/verkoop', view_func=self.verkoop)
        self.views.add_url_rule('/inkoop', view_func=self.inkoop)
        self.views.add_url_rule('/bestelgeschiedenis', view_func=self.bestelgeschiedenis)
        self.views.add_url_rule('/koeriers', view_func=self.koeriers)
        self.views.add_url_rule('/koeriers/klant-info/<int:klant_id>', methods=['GET', 'POST'], view_func=self.koeriers_klant_info)

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
        klanten = self._execute_query("SELECT klant_id, naam, adres, telefoonnummer, jaaromzet, website FROM klant")
        return render_template("klanten.html", klanten=klanten)

    # 📌 FINANCIËN
    def financien(self, klant_id):
        print(klant_id)
        klant_financien = self._execute_query("""
            SELECT 
                b.klant_id,
                b.bestelling_id, 
                b.status, 
                b.totaal_bedrag, 
                b.korting, 
                k.naam AS koerier,
                b.levermoment, 
                CASE 
                    WHEN b.spoed = 1 THEN 'Ja' 
                    ELSE 'Nee' 
                END AS spoed,
                GROUP_CONCAT(p.naam ORDER BY p.naam SEPARATOR ', ') AS producten
            FROM bestellingen AS b
            JOIN bestellingregels AS br ON b.bestelling_id = br.bestelling_id
            JOIN products AS p ON br.product_id = p.product_id
            JOIN koeriers AS k ON b.koerier_id = k.koerier_id
            WHERE b.klant_id = %s
            GROUP BY b.bestelling_id;""", (klant_id,))
        
        klant = self._execute_query("""
            SELECT 
                k.naam
            FROM klant AS k
            WHERE k.klant_id = %s;""", (klant_id,))
        print(klant_financien)
        if not klant_financien:
            return "Klant niet gevonden", 404

        return render_template("financien.html", financien=klant_financien, klant=klant)

    def financien_toevoegen(self):
        if request.method == 'POST':
            klant_id = request.form.get('klant')
            status = request.form.get('status')
            bedrag = request.form.get('bedrag')
            korting = request.form.get('korting')
            koerier = request.form.get('koerier')
            levermoment = request.form.get('levermoment')
            spoed = request.form.get('spoed')
            producten = request.form.getlist('producten')
            datum = datetime.now().strftime("%Y-%m-%d")
            if not klant_id.isdigit():
                return "Ongeldig klant ID.", 400
            print(klant_id, status, bedrag, korting, koerier, levermoment, spoed, producten)
            self._execute_query("""
                INSERT INTO bestellingen (klant_id, datum, status, totaal_bedrag, korting, koerier_id, levermoment, spoed ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (klant_id, datum, status, bedrag, korting, koerier, levermoment, spoed))
            bestelling_id = self._execute_query("SELECT max(bestelling_id) FROM bestellingen;")
            for product in producten:
                self._execute_query("""
                    INSERT INTO bestellingregels (bestelling_id, product_id)
                    VALUES (%s, %s)
                """, (bestelling_id, product))

            return redirect(url_for('views.financien', klant_id=klant_id))
        koeriers = self._execute_query("SELECT koerier_id, naam FROM koeriers")
        producten = self._execute_query("SELECT product_id, naam FROM products")
        klanten = self._execute_query("SELECT klant_id, naam FROM klant")
        return render_template("financien_toevoegen.html", klanten=klanten, koeriers=koeriers, producten=producten)

    def financien_wijzigen(self, financien_id):
        klant_financien = self._execute_query("""
                    SELECT 
                        b.status, 
                        b.totaal_bedrag, 
                        b.korting, 
                        k.naam AS koerier,
                        b.levermoment, 
                        b.spoed,
                        GROUP_CONCAT(p.naam ORDER BY p.naam SEPARATOR ', ') AS producten
                    FROM bestellingen AS b
                    JOIN bestellingregels AS br ON b.bestelling_id = br.bestelling_id
                    JOIN products AS p ON br.product_id = p.product_id
                    JOIN koeriers AS k ON b.koerier_id = k.koerier_id
                    WHERE b.bestelling_id = %s
                    GROUP BY b.bestelling_id;""", (financien_id,))
        koeriers = self._execute_query("SELECT koerier_id, naam FROM koeriers")
        print(klant_financien)
        if request.method == 'POST':
            status = request.form.get('status')
            bedrag = request.form.get('bedrag')
            korting = request.form.get('korting')
            koerier = request.form.get('koerier')
            levermoment = request.form.get('levermoment')
            spoed = request.form.get('spoed')
            # print(status, bedrag, korting, koerier, levermoment, spoed, financien_id)
            self._execute_query("""
                    UPDATE bestellingen
                    SET status = %s, totaal_bedrag = %s, korting = %s, koerier_id = %s, levermoment = %s, spoed = %s
                    WHERE bestelling_id = %s
                """,(status, bedrag, korting, koerier, levermoment, spoed, financien_id))

        return render_template("financien_wijzigen.html", financien_id=financien_id, koeriers=koeriers, financien=klant_financien)

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
            naam = request.form['naam']
            beschrijving = request.form['beschrijving']
            prijs = request.form['prijs']
            gewicht = request.form['gewicht']
            categorie = request.form['categorie']
            bewaaradvies = request.form['bewaaradvies']
            bederfelijkheid = request.form['bederfelijkheid']
            print(naam, beschrijving, prijs, gewicht, categorie, bewaaradvies, bederfelijkheid)
            self._execute_query("""
                INSERT INTO products (naam, beschrijving, prijs, gewicht, categorie, bewaaradvies, bederfelijkheidsfactor) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (naam, beschrijving, prijs, gewicht, categorie, bewaaradvies, bederfelijkheid))

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
            SELECT k.klant_id, b.bestelling_id, b.datum, k.naam, k.adres, c.naam 
            FROM bestellingen b
            JOIN klant k ON b.klant_id = k.klant_id
            JOIN koeriers c ON b.koerier_id = c.koerier_id
            ORDER BY b.bestelling_id
        """)
        return render_template("koeriers.html", koeriers=koeriers_data, leveringen=leveringen)

    def koeriers_klant_info(self, klant_id):
        if request.method == 'POST':
            naam = request.form['klant_naam']
            adres = request.form['klant_adres']
            telefoon = request.form['klant_telefoon']
            website = request.form['klant_website']
            jaaromzet = request.form['klant_jaaromzet']
            self._execute_query("""
                UPDATE klant 
                SET naam = %s, adres = %s, telefoonnummer = %s, jaaromzet = %s, website = %s
                WHERE klant_id = %s
            """, (naam, adres, telefoon, jaaromzet, website, klant_id))
        klant = self._execute_query("SELECT * FROM klant WHERE klant_id = %s", (klant_id,))
        koerier_info = self._execute_query("SELECT * FROM koeriers WHERE koerier_id = %s", (klant_id,))
        return render_template("koeriers_klant_info.html", klant_id=klant_id, klant=klant, koerier_info=koerier_info)
from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

# Required
app.config['MYSQL_HOST'] = 'mysql.atd.avans.nl'
app.config['MYSQL_USER'] = 's2233725'
app.config['MYSQL_PASSWORD'] = 's2233725'
app.config['MYSQL_DB'] = 's2233725'
mysql = MySQL(app)

@app.route("/")

def users():
    cur = mysql.connection.cursor()
    cur.execute("""Select * from autozaak.klanten""")
    rv = cur.fetchall()
    print(rv)
    return str(rv)

if __name__ == "__main__":
    app.run(debug=True)
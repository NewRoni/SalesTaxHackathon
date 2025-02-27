from flask import Flask, render_template, request, session
import flask_session
import sqlite3

app = Flask(__name__)

app.secret_key = "usercrypt"

# Starts a user session and greets the user with an input box
@app.route('/', methods=['POST', 'GET'])
def Main():
    result = None
    if request.method == 'POST':
        session.permanent = True

        state = request.form.get('State')
        price = request.form.get('Price')

        if not state or not price:
            result = "Please fill blank fields"
        else:
            try:
                price = int(price)

                session['state'] = state
                session['price'] = price
            except ValueError:
                print("Price must be a number")
        sessionid = request.cookies.get('session')
        print(sessionid)
        
    return render_template('Main.html', result=result)


DB_NAME = 'SaleTax.db'

with sqlite3.connect(DB_NAME) as db:
  pass

def CreateHistoryTable():
  conn = sqlite3.connect(DB_NAME)
  curs = conn.cursor()
  curs.execute("CREATE TABLE History (user_session CHAR(95) NOT NULL PRIMARY KEY, destination VARCHAR(29) NOT NULL, product VARCHAR(120) NOT NULL, type VARCHAR(120), product_price FLOAT NOT NULL, product_quantity INT, tax_paid FLOAT NOT NULL)")
  conn.commit()
  conn.close()
  print("History Table created")


def TaxHistory(user_session, destination, product, type, product_price, product_quantity, tax_paid):
  conn = sqlite3.connect(DB_NAME)
  curs = conn.cursor()
  curs.execute('INSERT INTO History (user_session, destination, product, type, product_price, product_quantity, tax_paid) VALUES (?, ?, ?, ?, ?, ?, ?) ON CONFLICT DO NOTHING', (user_session, destination, product, type, product_price, product_quantity, tax_paid))
  print('History added')
  conn.commit()
  conn.close()

def CallHistory():
  conn = sqlite3.connect(DB_NAME)
  curs = conn.cursor()
  curs.execute('SELECT * FROM History')
  rows = curs.fetchall()
  for i in rows:
    print(i)
  conn.close()

def DeleteHistoryTable():
  conn = sqlite3.connect(DB_NAME)
  curs = conn.cursor()
  curs.execute('DROP TABLE History')
  conn.commit()
  conn.close()
  print('History Table Deleted')



#DeleteHistoryTable()
#CreateHistoryTable()
TaxHistory('eyJfcGVybWFuZW50Ijp0cnVlLCJwcmljZSI6MTksInN0YXRlIjoiT2hpbyJ9.Z8B7Zw.S_EX5r9nTm3xvBKkUqQsswKE0Wk', 'Ohio', 'gift card', 'inheritance', 19, 2, 1.99)
CallHistory()

if __name__ == "__main__":
    app.run(use_reloader = True, debug=True, host="0.0.0.0", port = 8001)

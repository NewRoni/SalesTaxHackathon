from flask import Flask, render_template, request, session
import flask_session
import sqlite3
import uuid

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
        quantity = request.form.get('Quantity')
        name = request.form.get('Name')
        product = request.form.get('Product')

        if not state or not price or not quantity or not name or not product:
            result = "Please fill blank fields"
        else:
            try:
                price = float(price)
                quantity = int(quantity)

                session['state'] = state
                session['price'] = price
                session['quantity'] = quantity
                session['name'] = name
                session['product'] = product
            except ValueError:
                result = "Ensure Price and quantity are both numbers"
        sessionid = request.cookies.get('session')
        print(sessionid)
        print(session)
        
    return render_template('Main.html', result=result)


DB_NAME = 'SalesTax.db'

with sqlite3.connect(DB_NAME) as db:
  pass

# calculation_id = str(uuid.uuid4()) # when form submitted, generate 

def CreateHistoryTable():
  conn = sqlite3.connect(DB_NAME)
  curs = conn.cursor()
  curs.execute("CREATE TABLE History (calculation_id CHAR(36) NOT NULL PRIMARY KEY, user_session CHAR(95) NOT NULL, destination VARCHAR(29) NOT NULL, product VARCHAR(120) NOT NULL, type VARCHAR(120), product_price FLOAT NOT NULL, product_quantity INT, tax_paid FLOAT NOT NULL)")
  conn.commit()
  conn.close()
  print("History Table created")


def TaxHistory(calculation_id, user_session, destination, product, type, product_price, product_quantity, tax_paid):
  conn = sqlite3.connect(DB_NAME)
  curs = conn.cursor()
  curs.execute('INSERT INTO History (calculation_id, user_session, destination, product, type, product_price, product_quantity, tax_paid) VALUES (?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT DO NOTHING', (calculation_id, user_session, destination, product, type, product_price, product_quantity, tax_paid))
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
#TaxHistory(calculation_id,'eyJfcGVybWFuZW50Ijp0cnVlLCJwcmljZSI6MTksInN0YXRlIjoiT2hpbyJ9.Z8B7Zw.S_EX5r9nTm3xvBKkUqQsswKE0Wk', 'Ohio', 'gift card', 'inheritance', 19, 2, 1.99)
#CallHistory()


if __name__ == "__main__":
    app.run(use_reloader = True, debug=True, host="0.0.0.0", port = 8001)

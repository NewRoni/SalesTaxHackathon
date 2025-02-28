from flask import Flask, render_template, request, session, jsonify
from training import load_model
from product_clf.preprocess import preprocess
import flask_session
import sqlite3, uuid
import ml_utilities as ml
import pandas as pd
import json

config = json.load(open('config.json', 'r'))
tax_model = load_model(f"{config['tax_model_dir']}/model.pkl")
encoder = load_model(f"{config['tax_model_dir']}/encoder.pkl")

text_model = load_model(f"{config['text_model_dir']}/product_clf.pkl")
lb_encoder = load_model(f"{config['text_model_dir']}/label_encoder.pkl")

# basic_rates = json.load(open('data/basic_rates.json', 'r'))

app = Flask(__name__)

app.secret_key = "usercrypt"

@app.route('/', methods=['POST', 'GET'])
def Main():
    result = None
    if request.method == 'POST':
        session.permanent = True
      
        state = request.form.get('state')
        price = request.form.get('Price')
        quantity = request.form.get('Quantity')
        name = request.form.get('Name')

        if not state or not price or not quantity or not name:
            result = "Please fill blank fields"
        else:
            try:
                price = float(price)
                quantity = int(quantity)

                session['state'] = state
                session['price'] = price
                session['quantity'] = quantity
                session['name'] = name
    
            except ValueError:
                result = "Ensure Price and quantity are both numbers"
        
    return render_template('main_update.html', result=result)

@app.route('/save_calculation', methods=['POST'])
def save_calculation():
    if request.method == "POST":
        data = request.get_json()
        calculation_id = str(uuid.uuid4())
        user_session = request.cookies.get('session')
        
        itemName = data.get('itemName')
        price = data.get('price')
        quantity = data.get('quantity')
        product_type = data.get('product_type')
        state = data.get('state')
        tax_paid = data.get('tax_paid')
        
        if not all([itemName, price, quantity, state, product_type, tax_paid]):
            return jsonify({'error': 'Missing data in request'}), 400

        try:
            TaxHistory(calculation_id, user_session, state, itemName, product_type, float(price), int(quantity), float(tax_paid))
            return jsonify({'message': 'Calculation saved successfully!'})
        except Exception as e:
            return jsonify({'error': f'Database error: {e}'}), 500

@app.route('/text_inference', methods=['POST'])
def text_inference():
    product_name = request.form['product_name']
    class_names = lb_encoder.classes_
    
    input_df = pd.DataFrame({
        "product_name": [product_name]
    })
    X = preprocess(input_df, mode="inference")
    y_pred = ml.predict(text_model, X)[0]
    print(y_pred)
    return class_names[y_pred]
    

@app.route('/tax_inference', methods=['POST'])
def inference():
    try:
        state = str(request.form['state']).title()
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        product_type = request.form.get('product_type')
        product_type = 'General' if not product_type else str(product_type).title()
        
        input_df = pd.DataFrame({
            "state": [state],
            "product_type": [product_type]
        })
        X = encoder.transform(input_df)
        tax_rate = ml.predict(tax_model, X)[0]
        tax_rate = abs(round(tax_rate, 4))

        pretax_cost = price * quantity
        total_tax = pretax_cost * tax_rate
        total_price = pretax_cost + total_tax
        print(f"<<Total: {total_price}>>")
        
        return jsonify({
                'tax_rate': f"{tax_rate * 100:.2f}%",
                'total_tax': f"{total_tax:.2f}",
                'total_price': f"{total_price:.2f}"
            })
    except (KeyError, ValueError, TypeError) as e:
        return jsonify({'error': f"Invalid input: {e}"}), 400
    except Exception as e:
        return jsonify({'error': f"An unexpected error occurred: {e}"}), 500
    
DB_NAME = 'SalesTax.db'

with sqlite3.connect(DB_NAME) as db:
  pass

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
  curs.execute('INSERT INTO History (calculation_id, user_session, destination, product, type, product_price, product_quantity, tax_paid) VALUES (?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT DO NOTHING',
               (calculation_id, user_session, destination, product, type, product_price, product_quantity, tax_paid))
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
    app.run(use_reloader = True, debug=True, host="0.0.0.0")
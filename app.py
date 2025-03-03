from flask import Flask, render_template, request, session, jsonify
import flask_session
from training import load_model
from product_clf.preprocess import preprocess
import sqlite3
import uuid
import ml_utilities as ml
import pandas as pd
import json

config = json.load(open('config.json', 'r'))
tax_model = load_model(f"{config['tax_model_dir']}/model3.pkl")
encoder = load_model(f"{config['tax_model_dir']}/encoder.pkl")

text_model = load_model(f"{config['text_model_dir']}/product_clf.pkl")
lb_encoder = load_model(f"{config['text_model_dir']}/label_encoder.pkl")

app = Flask(__name__)

app.secret_key = "usercrypt"
session_id = ''

def check_session(f):
    def decorated_function(*args, **kwargs):
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4()) # generate session id
            session.permanent = True
        else:
            # DeleteHistoryTable()
            # CreateHistoryTable()
            history = CallHistory()
            user_logs = [[log[2].title()] + list(log[3:]) for log in history if log[1] == session['session_id']]
            user_logs = list(reversed(user_logs))
            kwargs['user_logs'] = user_logs
            print(user_logs)
        return f(*args, **kwargs)
    return decorated_function

# Starts a user session and greets the user with an input box
@app.route('/')
@check_session
def Main(user_logs):
    global session_id
    session_id = session['session_id']
    print(f"Session id: {session_id}")
    top_3_states = StateTotalTax()
    
    return render_template('Main.html', logs=user_logs, top_3_states = top_3_states)

@app.route('/save_calculation', methods=['POST'])
def save_calculation():
    if request.method == "POST":
        data = request.get_json()
        calculation_id = str(uuid.uuid4())
        global session_id
        
        itemName = data.get('itemName')
        price = data.get('price')
        quantity = data.get('quantity')
        product_type = data.get('product_type')
        state = data.get('state')
        tax_paid = data.get('tax_paid')
        
        if not all([itemName, price, quantity, state, product_type, tax_paid]):
            return jsonify({'error': 'Missing data in request'}), 400

        try:
            TaxHistory(calculation_id, session_id, state, itemName, product_type, float(price), int(quantity), float(tax_paid))
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
                'tax_rate': f"{tax_rate * 100:.2f}", # tax rate in percent
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

@app.route('/top_cost_states', methods= ['GET', 'POST'])
def StateTotalTax():
    state_tax_dict = {}
    
    history = CallHistory()
    user_logs = [[log[2].title()] + list(log[3:]) for log in history if log[1] == session['session_id']]

    for log in user_logs:
        state = log[0]
        tax = log[-1]

        if state not in state_tax_dict:
            state_tax_dict[state] = tax
        else:
            state_tax_dict[state] += tax 

    sorted_dict = sorted(state_tax_dict.items(), key=lambda t: t[1], reverse=True)

    top_3_state_cost = []

    for state, tax in sorted_dict[:3]:  # Get only the top 3
        top_3_state_cost.append((state, tax))  # Append as tuple

    return top_3_state_cost


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
  conn.close()
  return rows

def DeleteHistoryTable():
  conn = sqlite3.connect(DB_NAME)
  curs = conn.cursor()
  curs.execute('DROP TABLE History')
  conn.commit()
  conn.close()
  print('History Table Deleted')




#DeleteHistoryTable()
#CreateHistoryTable()
#CallHistory()


if __name__ == "__main__":
    app.run(use_reloader = True, debug=True, host="0.0.0.0", port = 8001)
    

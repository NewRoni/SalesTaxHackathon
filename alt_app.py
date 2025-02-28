from flask import Flask, render_template, request
from training import load_model
import ml_utilities as ml
import pandas as pd
import json

app = Flask(__name__)
model = load_model('tax_models/model.pkl')
encoder = load_model('tax_models/encoder.pkl')
basic_rates = json.load(open('data/basic_rates.json', 'r'))

@app.route('/')
def Main():
    return render_template('Main.html')

@app.route('/inference', methods=['POST'])
def inference():
    state = request.form['state'].title()
    price = float(request.form['price'])
    quantity = int(request.form['quantity'])
    product_type = request.form.get('product_type')
    product_type = 'General' if not product_type else product_type.title()
    
    input_df = pd.DataFrame({
        "state": [state],
        "product_type": [product_type]
    })
    X = encoder.transform(input_df)
    tax_rate =  ml.predict(model, X)[0]

    pretax_cost = price * quantity
    final_cost = pretax_cost + (pretax_cost * tax_rate)
    
    
    return f"Original Cost{pretax_cost:.2f} | Tax rate: {tax_rate:.3f} | Final Cost: {final_cost:.2f}"

if __name__ == "__main__":
    app.run(use_reloader = True, debug=True, host="0.0.0.0")
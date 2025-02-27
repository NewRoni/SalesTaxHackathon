from flask import Flask, render_template, request, session
import flask_session

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

if __name__ == "__main__":
    app.run(use_reloader = True, debug=True, host="0.0.0.0", port = 8001)

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

        if not state or not price:
            result = "Please fill blank fields"
        else:
            try:
                price = int(price)

                session['state'] = state
                session['price'] = price
            except ValueError:
                print("Price must be a number")
        
    return render_template('Main.html', result=result)

if __name__ == "__main__":
    app.run(use_reloader = True, debug=True, host="0.0.0.0", port = 8001)

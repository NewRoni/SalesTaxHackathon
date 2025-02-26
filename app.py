from flask import Flask, render_template, request, session
app = Flask(__name__)

app.secret_key = "usercrypt"
session = ["My Tax"]

# Starts a user session and greets the user with an input box
@app.route('/', methods=['POST', 'GET'])
def Main():
    result = None
    if request.method == 'POST':
        session.permanent = True
        try:
            text = request.form['State']
            text = str(text)
        except ValueError:
            result = "invalid input"

    return render_template('Main.html', result=result)



if __name__ == "__main__":
    app.run(use_reloader = True, debug=True, host="0.0.0.0")

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def Main():
    result = None
    if request.method == 'POST':
        try:
            text = request.form['State']
            text = String(text)
        except ValueError:
            result = "invalid input"

    return render_template('Main.html', result=result)



if __name__ == "__main__":
    app.run(use_reloader = True, debug=True, host="0.0.0.0")

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def Main():
    return render_template('Main.html')

if __name__ == "__main__":
    app.run(use_reloader = True, debug=True, host="0.0.0.0")
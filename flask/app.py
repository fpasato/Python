import time
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home/index.html", t=int(time.time()))

@app.route("/register")
def register():
    return render_template("register/index.html", t=int(time.time()))


if __name__ == "__main__":
    app.run(debug=True)  
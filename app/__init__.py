from flask import Flask, render_template
import os

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def root():
    return render_template("home.html")


if(__name__ == "__main__"):
    app.debug = False
    app.run()

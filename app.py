from flask import Flask, request, render_template
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/inspirations")
def inspirations_page():
    return render_template("inspirations.html")

@app.route("/encrypt")
def encrypt_page():
    return render_template("encrypt.html")
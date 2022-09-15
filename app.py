# import os
from flask import Flask, request, render_template, url_for, redirect
# from markupsafe import escape

app = Flask(__name__)


def file_encryption():
    pass


@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/inspirations")
def inspirations_page():
    return render_template("inspirations.html")


@app.get("/encrypt")
def encrypt_page():
    return render_template("encrypt.html")


@app.post("/encrypt")
def encrypt_file():
    if "file" not in request.files:
        return "Error: No File Part"

    file = request.files["file"]

    if file.filename == "":
        return "Error: No File Selected"

    print(file.filename, flush=True)

    return file.read()
    # return redirect(url_for("download_page"))


@app.route("/download")
def download_page(file):
    file_binary = file.read()
    return render_template("download.html")

import sqlite3
import logging
import os
import sys
from flask import Flask, session, redirect, url_for, request, render_template, abort
from flask_status import FlaskStatus
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

secret_key = os.environ.get("FLASK_SECRET_KEY")
# Secret key needs to be stable; Fail if it's not set up beforehand.
if not secret_key:
    app.logger.error("Missing required environment variable FLASK_SECRET_KEY")
    sys.exit(1)
app.secret_key = secret_key

# Enable CSRF protection (include tokens in requests)
csrf = CSRFProtect(app)

# make sure templates are rendered with autoescape
app.jinja_options["autoescape"] = True

# create ping/status endpoint
FlaskStatus(app, url="/ping")


def get_db_connection():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    return connection


def is_authenticated():
    if "username" in session:
        return True
    return False


def authenticate(username, password):
    connection = get_db_connection()
    users = connection.execute("SELECT * FROM users").fetchall()
    connection.close()

    for user in users:
        if user["username"] == username and user["password"] == password:
            app.logger.info(f"the user '{username}' logged in successfully.")
            session["username"] = username
            return True

    app.logger.warning(f"the user '{ username }' failed to log in.")
    abort(401)


@app.route("/")
def index():
    return render_template("index.html", is_authenticated=is_authenticated())


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if authenticate(username, password):
            return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

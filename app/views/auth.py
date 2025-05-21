from flask import Blueprint, session, redirect, url_for, request, flash, render_template
from flask_dance.contrib.google import google
import json
from .. import socketio
import logging

logging.basicConfig(level=logging.DEBUG)

bp = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/auth",
)


@bp.route("/", methods=["GET"])
def index():
    return render_template("auth/signup.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "password":
            session["logged_in"] = True
            session["username"] = username
            flash("Successfully logged in.", "success")
            return redirect(url_for("main.index"))
        else:
            flash("Invalid username or password.", "danger")

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))


@bp.route("/register", methods=["GET"])
def register():
    return render_template("auth/register.html")


@bp.route("/google")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    user_info = resp.json()

    session["user"] = {
        "email": user_info["email"],
        "name": user_info["name"],
        "picture": user_info.get("picture"),
    }
    return redirect(url_for("main.index"))

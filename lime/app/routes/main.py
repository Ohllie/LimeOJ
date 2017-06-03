from flask import session, request, render_template, flash, redirect, Blueprint, send_from_directory, abort

import os

from helpers import get_current_revision, redirect_url
from models import *
from constants import *

main = Blueprint('main', __name__, template_folder='../templates')

@main.route('/')
def home():
  return render_template("home.html", rev=get_current_revision())

@main.route('/register', methods=["GET", "POST"])
def register():

  if request.method == "POST":

    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
      return redirect(redirect_url())

    accs = User.query.filter(User.username == username).all()

    if len(accs):
      flash("Username is taken", "error")
      return redirect(redirect_url())

    user = User()
    user.username = username
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    flash("Success!", "success")

  return render_template("register.html")

@main.route('/login', methods=["GET", "POST"])
def login():

  if request.method == "POST":

    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
      flash("Username and password are required to log in", "error")
      return redirect(redirect_url())

    accs = User.query.filter(User.username == username).all()

    if not len(accs):
      flash(APP_INVALID_PASSWORD)
      return redirect(redirect_url())

    acc = accs[0]

    if acc.verify_password(password):
      flash("Right!", "success")
    else:
      flash("Wrong!", "error")

  return render_template("login.html")

@main.route('/problems')
def problems():
  return render_template("problems.html")

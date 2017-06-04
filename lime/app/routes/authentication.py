from flask import session, request, render_template, flash, redirect, Blueprint, send_from_directory, abort, url_for

from helpers import get_current_revision, redirect_url
from models import *
from constants import *
from auth import authorized, serialize_session
from database import db, session_scope

auth = Blueprint('auth', __name__, template_folder='../templates')


@auth.route('/register', methods=["GET", "POST"])
def register():

  if request.method == "POST":

    username = request.form.get("username")
    password = request.form.get("password")
    rpassword = request.form.get("rpassword")

    print(username, password, rpassword)

    if any(x is None or len(x) == 0 for x in [username, password, rpassword]):
      flash("Please fill in all the fields", "error")
      return redirect(redirect_url())

    if password != rpassword:
      flash("Passwords did not match!", "error")
      return redirect(redirect_url())

    accs = User.query.filter(User.username == username).all()

    if len(accs):
      flash("Username '{}' is taken".format(username), "error")
      return redirect(redirect_url())

    user = User()
    user.username = username
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    # set session

    session["user"] = serialize_session(user)
    flash("Welcome, {}!".format(username), "success")

    return redirect(url_for("main.home"))

  return render_template("register.html")


@auth.route('/login', methods=["GET", "POST"])
def login():

  if request.method == "POST":

    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
      flash("Username and password are required to log in", "error")
      return redirect(redirect_url())

    accs = User.query.filter(User.username == username).all()

    if not len(accs):
      flash(APP_INVALID_PASSWORD, "error")
      return redirect(redirect_url())

    acc = accs[0]

    if acc.verify_password(password):
      # set the session variables

      session["user"] = serialize_session(acc)
      flash("Welcome, {}!".format(username), "success")

      return redirect(url_for("main.home"))

    flash(APP_INVALID_PASSWORD, "error")

  return render_template("login.html")


@auth.route('/logout')
@authorized()
def logout():

  # clear the session and redirect
  del session["user"]

  flash("Logged out successfully", "success")
  return redirect(url_for("main.home"))

from flask import session, request, render_template, flash, redirect, Blueprint

main = Blueprint('main', __name__, template_folder='../templates')

@main.route('/')
def home():
  return render_template("home.html")

@main.route('/login', methods=["GET"])
def login():
  return render_template("login.html")

@main.route('/problems')
def problems():
  return render_template("problems.html")
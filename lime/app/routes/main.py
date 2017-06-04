import os

from flask import session, request, render_template, flash, redirect, Blueprint, send_from_directory, abort, url_for

from helpers import get_current_revision, redirect_url
from models import *
from constants import *
from auth import authorized, serialize_session
from database import db, session_scope

main = Blueprint('main', __name__, template_folder='../templates')


@main.route('/')
def home():
  return render_template("home.html", rev=get_current_revision())


@main.route('/problems')
def problems():

  problems = []

  with session_scope() as session:
    problems = [p.serialize() for p in session.query(Problem).all()]

  return render_template("problems.html", problems=problems)


@main.route('/profile')
@authorized()
def profile():
  user_id = session["user"]

  return render_template("base.html")

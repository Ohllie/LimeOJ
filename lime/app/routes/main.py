import os

from flask import session, request, render_template, flash, redirect, Blueprint, send_from_directory, abort, url_for

from helpers import get_current_revision, redirect_url, serialized
from models import *
from constants import *
from auth import authorized, serialize_session
from database import db, session_scope

main = Blueprint('main', __name__, template_folder='../templates')


@main.route('/')
def home():
  return render_template("home.html", rev=get_current_revision())


@main.route('/profile')
@authorized()
def profile():

  user_data = session["user"]
  user = None
  submissions = []

  with session_scope() as s:
    user = User.query.filter(User.id == user_data["id"]).first_or_404()

    submissions = serialized(
      user.submissions.join(Problem).order_by(Submission.created_at.desc()).all(),
      extra=["problem"]
    )

    user = user.serialize()

  return render_template("profile.html", user=user, submissions=submissions)

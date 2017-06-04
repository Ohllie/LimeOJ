from flask import Flask, render_template, g, request, flash, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

from datetime import timedelta
from database import db

from os.path import join, dirname
from dotenv import load_dotenv

import os
import sys

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

if not os.environ.get("FLASK_SECRET", False):
  print("FLASK_SECRET not set in .env!")
  sys.exit(1)

if not os.environ.get("DB_URL", False):
  print("DB_URL not set in .env!")
  sys.exit(1)


def create_app():

  app = Flask(__name__)

  app.secret_key = os.environ.get("FLASK_SECRET")

  # suppress the overhead warning
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")

  # configure the server-side sessions
  app.config["SESSION_TYPE"] = "sqlalchemy"
  app.config["SESSION_SQLALCHEMY"] = db
  app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=60 * 24 * 30)

  app.debug = True

  db.init_app(app)

  from routes.main import main
  app.register_blueprint(main)

  from routes.authentication import auth
  app.register_blueprint(auth)

  from routes.problem import problem
  app.register_blueprint(problem)

  try:
    from routes.test import test
    app.register_blueprint(test)
  except ImportError:
    # if the test route file doesn't exist, just don't register the routes
    pass

  @app.errorhandler(404)
  def page_not_found(e):
    return render_template('404.html'), 404

  from auth import logged_in
  app.add_template_global(logged_in)

  from constants import VALID_LANGS

  def valid_langs():
    return VALID_LANGS.items()

  app.add_template_global(valid_langs)

  sess = Session()
  sess.init_app(app)

  return app

if __name__ == '__main__':
  app = create_app()
  app.run(threaded=True, host="0.0.0.0", port=80, debug=True)

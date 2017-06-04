from flask import session, request, render_template, flash, redirect, Blueprint, send_from_directory, abort, url_for

from helpers import get_current_revision, redirect_url
from models import *
from constants import *
from auth import authorized, serialize_session
from database import db, session_scope

problem = Blueprint('problem', __name__, template_folder='../templates')


@problem.route('/problem/<id>')
def view(id):

  problem = None
  examples = []

  with session_scope() as session:
    problem = Problem.query.filter(Problem.id == id).first_or_404()
    examples = [t.serialize() for t in problem.tests.filter(Test.example).all()]

    problem = problem.serialize()

  return render_template("problem.html", problem=problem, examples=examples)


@problem.route('/problems')
def list():

  problems = []

  with session_scope() as session:
    problems = [p.serialize() for p in session.query(Problem).all()]

  return render_template("problems.html", problems=problems)

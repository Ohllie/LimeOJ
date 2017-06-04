from flask import session, request, render_template, flash, redirect,\
    Blueprint, send_from_directory, abort, url_for, request

from helpers import get_current_revision, redirect_url
from models import *
from constants import *
from auth import authorized, serialize_session
from database import db, session_scope, transaction

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


@problem.route('/problem/<id>/submit', methods=["POST"])
@transaction
@authorized()
def submit(s, id):
  problem = s.query(Problem).filter(Problem.id == id).first_or_404()
  problem_s = problem.serialize()

  def ret():
    return render_template("problem.html", problem=problem_s)

  if "filetype" not in request.form:
    flash("No filetype selected!", "error")
    return ret()

  filetype = request.form["filetype"]

  if filetype not in VALID_LANGS.values():
    flash("Selected filetype is not valid!", "error")
    return ret()

  if "file" not in request.files:
    flash("No file supplied!", "warning")
    return ret()

  file = request.files["file"]

  if file.filename == "" or not file:
    flash("No file supplied!", "warning")
    return ret()

  extension = file.filename.split(".")[-1]
  if extension not in ["cpp", "c++", "cc"]:
    flash("The file you submitted has an invalid extension", "error")
    return ret()

  try:
    code = file.read().decode("utf-8")
  except:
    flash("The file you submitted did not contain UTF-8 encoded text!", "error")
    return ret()

  # create the new submission
  sub = Submission()
  sub.user_id = session["user"]["id"]
  sub.language = request.form["filetype"]
  sub.problem_id = problem_s["id"]
  sub.code = code
  sub.status = STATUS_IN_QUEUE
  sub.result = RESULT_ND
  sub.tests_done = 0
  sub.tests_total = len(problem.tests.all())

  s.add(sub)

  flash("Submission successful!", "success")
  return render_template("problem.html", problem=problem_s)


@problem.route('/submission/<id>')
@transaction
@authorized()
def view_submission(s, id):
  s = Submission.query.filter(Submission.id == id).first_or_404()

  return render_template("submission.html", submission=s.serialize())


@problem.route('/problems')
def list():

  problems = []

  with session_scope() as session:
    problems = [p.serialize() for p in session.query(Problem).all()]

  return render_template("problems.html", problems=problems)

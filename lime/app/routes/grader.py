import base64

from flask import session, request, render_template, flash,\
  redirect, Blueprint, send_from_directory, abort, url_for, jsonify

from functools import wraps

from helpers import get_current_revision, redirect_url, serialized
from models import *
from constants import *
from auth import authorized, serialize_session
from database import db, session_scope, transaction

grader = Blueprint('grader', __name__, template_folder='../templates')


def grader_api(f):
  ''' A decorator for limiting the access of the grader routes '''

  @wraps(f)
  def w(*args, **kwargs):

    if request.remote_addr != "127.0.0.1":
      abort(403)

    return f(*args, **kwargs)
  return w


@grader.route("/grader/queue")
@transaction
@grader_api
def submissions(session):
  queue = Submission.query.filter(Submission.status == STATUS_IN_QUEUE)
  ids = [item.id for item in queue]
  return jsonify(ids)


@grader.route("/grader/<id>/start")
@transaction
@grader_api
def start(session, id):
  s = session.query(Submission).filter(Submission.id == id).first_or_404()

  if s.status != STATUS_IN_QUEUE:
    abort(400)

  s.status = STATUS_TESTING
  session.add(s)
  return jsonify({"message": "ok"})


@grader.route("/grader/<id>/data")
@transaction
@grader_api
def data(session, id):

  s = session.query(Submission).filter(Submission.id == id).first_or_404()
  p = session.query(Problem).filter(Submission.problem_id == Problem.id).first()

  if not p:
    abort(400)

  test_ids = [x.id for x in p.tests.all()]

  if not test_ids or not len(test_ids):
    abort(400)

  return jsonify({
    "grader": p.grader,
    "test_ids": test_ids,
    "code": s.code,
    "lang": s.language,
    "time_limit": p.time_limit,
    "memory_limit": p.memory_limit
  })


@grader.route("/grader/<id>/result")
@transaction
@grader_api
def result(session, id):

  s = session.query(Submission).filter(Submission.id == id).first_or_404()

  if s.status != STATUS_TESTING:
    abort(400)

  if "status" not in request.args and "result" not in request.args:
    abort(400)

  if "status" in request.args:
    s.status = int(request.args["status"])

  if "result" in request.args:
    s.result = int(request.args["result"])

  session.add(s)
  return jsonify({"message": "ok"})


@grader.route("/grader/testids")
@transaction
@grader_api
def testids(session):
  s = session.query(Test).all()
  ids = [x.id for x in s]
  return jsonify(ids)


@grader.route("/grader/<id>/testdata")
@transaction
@grader_api
def tests(session, id):
  test = session.query(Test).filter(Test.id == id).first_or_404()

  data = {
    "input": test.input.decode("ascii"),
    "output": test.output.decode("ascii")
  }

  return jsonify(data)


@grader.route("/grader/<id>/status")
@transaction
def status(session, id):
  s = session.query(Submission).filter(Submission.id == id).first_or_404()
  return jsonify({"status": s.status_long()})

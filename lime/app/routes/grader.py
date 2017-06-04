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
      abort(404)

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
  return "ok"


@grader.route("/grader/<id>/status")
@transaction
def status(session, id):
  s = session.query(Submission).filter(Submission.id == id).first_or_404()
  return s.status_long()

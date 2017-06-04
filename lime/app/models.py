from datetime import datetime

from database import db, session_scope
from crypto import pwd_context
from helpers import random_uid
from constants import *


def get_stamp():
  ''' Returns the current epoch time as an integer '''

  import time
  return int(time.time())


def attrdict(obj, keys):
  d = {}
  for key in keys:
    d[key] = getattr(obj, key)
  return d


# This is defined here explicitly so that drop_all will also drop the version table
class AlembicVersion(db.Model):
  __tablename__ = "alembic_version"

  version_num = db.Column(db.String(256), primary_key=True)


class User(db.Model):
  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key=True)

  username = db.Column(db.String(16), unique=True)
  password = db.Column(db.String(256), unique=False)

  created_at = db.Column(db.Integer, default=get_stamp)
  last_login = db.Column(db.Integer)

  def set_password(self, password):
    self.password = pwd_context.hash(password)

  def verify_password(self, password):
    return pwd_context.verify(password, self.password)

  def serialize(self):
    ''' Serialize the object into a single python dictionary '''

    return attrdict(self, ["id", "username", "created_at", "last_login"])


class Problem(db.Model):
  __tablename__ = "problems"

  id = db.Column(db.String(16), primary_key=True)
  title = db.Column(db.String(64))
  description = db.Column(db.Text())
  difficulty = db.Column(db.Enum("1", "2", "3", "4", "5"))
  grader = db.Column(db.Text())

  time_limit = db.Column(db.Float, default=1.0)
  memory_limit = db.Column(db.Integer, default=64)

  tests = db.relationship('Test', backref='problems', lazy='dynamic')

  def __init__(self):
    ''' Initializes the id field with a random, unused id '''

    self.id = random_uid()

    while self.uid_exists(self.id):
      self.id = random_uid()

  def uid_exists(self, uid):
    ''' Checks whether a problem with the given id exists in the database '''

    with session_scope() as session:
      return session.query(Problem).filter(Problem.id == uid).first() is not None
    return False

  def serialize(self):
    ''' Serialize the object into a single python dictionary '''

    return attrdict(self, ["id", "title", "description", "difficulty"])


class Test(db.Model):
  __tablename__ = "tests"

  id = db.Column(db.Integer, primary_key=True)
  problem_id = db.Column(db.String(12), db.ForeignKey('problems.id'))

  problem = db.relationship('Problem', foreign_keys='Test.problem_id')

  input = db.Column(db.Binary)
  output = db.Column(db.Binary)

  example = db.Column(db.Boolean)

  def serialize(self):
    ''' Serialize the object into a single python dictionary '''

    strs = attrdict(self, ["id", "problem_id", "example"])

    strs["input"] = self.input.decode("ascii")
    strs["output"] = self.output.decode("ascii")

    return strs


class Submission(db.Model):
  __tablename__ = "submissions"

  id = db.Column(db.Integer, primary_key=True)

  problem_id = db.Column(db.String(12), db.ForeignKey('problems.id'))
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

  code = db.Column(db.Text)
  language = db.Column(db.String(12), default=LANGUAGE_CPP11)

  status = db.Column(db.Integer)
  result = db.Column(db.Integer)

  tests_done = db.Column(db.Integer)
  tests_total = db.Column(db.Integer)

  created_at = db.Column(db.Integer, default=get_stamp)

  execution_time = db.Column(db.Float)
  code_length = db.Column(db.Integer)

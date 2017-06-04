import os
import sys

from flask_sqlalchemy import SQLAlchemy
from contextlib import contextmanager
from functools import wraps

db = SQLAlchemy()


def transaction(f):
  @wraps(f)
  def w(*args, **kwargs):
    with session_scope() as s:
      return f(s, *args, **kwargs)
  return w


@contextmanager
def session_scope():
  ''' Provide a transactional scope around a series of operations. '''

  session = db.session
  try:
    yield session
    session.commit()
  except:
    session.rollback()
    raise
  finally:
    session.close()

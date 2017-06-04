from flask import session, redirect, url_for, flash, render_template
from functools import wraps
from constants import *


def logged_in(access_level=ACCESS_USER):
  ''' Returns whether there's a valid session '''

  if "user" not in session:
    return False

  user = session["user"]

  if user and "access_level" not in user:
    return False

  return user["access_level"] >= access_level


def serialize_session(user):
  ''' Serialize the session from a user object '''

  return {
      "id": user.id,
      "username": user.username,
      "access_level": ACCESS_USER
    }


def authorized(access_level=ACCESS_USER):
  ''' Decorator factory for making routes with automatic decoration '''

  def decorator(f):
    @wraps(f)
    def decorated(*args, **kwargs):
      if not logged_in(access_level):
        return render_template("unauthorized.html"), 403
      return f(*args, **kwargs)
    return decorated
  return decorator

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

def authorized(f):
  ''' Decorator for making '''

  @wraps(f)
  def decorated(*args, **kwargs):
    if not logged_in():
      return render_template("unauthorized.html"), 403
    return f(*args, **kwargs)
  return decorated
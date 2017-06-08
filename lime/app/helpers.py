from flask import request, url_for

import subprocess
import string
import random
from datetime import datetime


def redirect_url(default='main.home'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)


def get_current_revision():
  try:
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode("utf-8")
  except:
    return ""


def serialized(l, extra=None):
  ''' Serializes a list of items '''

  return [item.serialize(extra=extra) for item in l]


def random_uid(length=4):
  charset = string.ascii_lowercase + string.ascii_uppercase + string.digits
  return "".join([random.choice(charset) for x in range(length)])


def epoch(stamp):
  return datetime.fromtimestamp(stamp).strftime('%c')

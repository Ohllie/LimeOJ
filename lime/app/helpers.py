from flask import request, url_for

import subprocess
import string
import random


def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)


def get_current_revision():
  return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode("utf-8")


def serialized(l):
  ''' Serializes a list of items '''

  return [item.serialize() for item in l]


def random_uid(length=4):
  charset = string.ascii_lowercase + string.ascii_uppercase + string.digits
  return "".join([random.choice(charset) for x in range(length)])

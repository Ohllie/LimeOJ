from flask import request, url_for

import subprocess


def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)


def get_current_revision():
  return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode("utf-8")

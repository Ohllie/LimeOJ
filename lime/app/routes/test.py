from flask import session, request, render_template, flash, redirect, Blueprint, send_from_directory, jsonify    

import os
from auth import authorized
from constants import *

test = Blueprint('test', __name__, template_folder='../templates')


@test.route('/test')
def testroute():
  return "test"


@test.route('/session')
@authorized(access_level=ACCESS_ADMIN)
def secrets():
  return jsonify(session["user"])

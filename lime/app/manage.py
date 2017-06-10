import os
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand, upgrade

from app import create_app
from database import db, session_scope
from helpers import *
from models import *
from constants import *

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def seed():
  ''' Seed the entire database '''

  if not prompt_bool("Are you sure you want to lose all your data?"):
    return

  print("Dropping tables")
  db.drop_all()

  print("Running migrations")
  upgrade()

  print("Seeding data")

  with session_scope() as session:
    u = User()
    u.username = "foobar"
    u.set_password("barfoo")

    session.add(u)

    problems = []

    p = Problem()
    p.title = "Squares"
    p.description = """
Given a list of numbers, return their **squares**.

The first line of the input contains n, the length of the list.<br>
The next line contains n space separated integers.
    """
    p.difficulty = "1"
    p.grader = """
import os
import sys

def main():
  if len(sys.argv) != 3:
    sys.exit(1)

  user_output_path = sys.argv[1]
  ref_output_path = sys.argv[2]

  with open(user_output_path) as f:
    user_output = f.read()

  with open(ref_output_path) as f:
    ref_output = f.read()

  if not user_output or not ref_output or len(user_output) == 0:
    sys.exit(1)

  us = [x for x in user_output.strip().split() if len(x)]
  rs = [x for x in ref_output.strip().split() if len(x)]

  if len(us) != len(rs):
    sys.exit(1)

  for i, x in enumerate(rs):
    if x != us[i]:
      sys.exit(1)

  sys.exit(0)

if __name__ == '__main__':
  main()
"""

    session.add(p)
    problems.append(p.id)

    t = Test()
    t.problem_id = problems[0]
    t.input = """5
1 2 3 4 5""".encode("ascii")
    t.output = "1 4 9 16 25".encode("ascii")
    t.example = True

    t = Test()
    t.problem_id = problems[0]
    t.input = """5
6 7 8 9 10""".encode("ascii")
    t.output = "36 49 64 81 100".encode("ascii")
    t.example = True

    s = Submission()
    s.problem_id = problems[0]
    s.user_id = 1
    s.code = "some code here"
    s.status = STATUS_IN_QUEUE
    s.result = RESULT_ND
    s.tests_done = 0
    s.tests_total = 12

    session.add(s)
    session.add(t)

  print("done")


if __name__ == '__main__':
    manager.run()

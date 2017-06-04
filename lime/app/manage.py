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

  if not prompt_bool("Are you sure you want to lose all your data"):
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

    for d in range(1, 6):
      p = Problem()
      p.title = "Test Problem {}".format(d)
      p.description = "Test Problem Description"
      p.difficulty = str(d)
      p.grader = "print(\"I'm a grader\")"

      session.add(p)
      problems.append(p.id)

    t = Test()
    t.problem_id = problems[0]
    t.input = "1 2 3 4 5".encode("ascii")
    t.output = "2 4 6 8 10".encode("ascii")
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

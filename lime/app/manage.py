import os
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand, upgrade

from app import create_app
from database import db, session_scope
from helpers import *
from models import *

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

    p = Problem()
    p.title = "Test Problem"
    p.description = "Test Problem Description"
    p.difficulty = "5"

    session.add(p)

  print("done")


if __name__ == '__main__':
    manager.run()

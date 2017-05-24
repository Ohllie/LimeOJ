from database import db
from datetime import datetime

def get_stamp():
  import time
  return int(time.time())

from crypto import pwd_context

class User(db.Model):
  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key=True)
  
  username = db.Column(db.String(16), unique=True)
  password = db.Column(db.String(256), unique=False)
  
  created_at = db.Column(db.Integer, default=get_stamp)
  last_login = db.Column(db.Integer)

  def set_password(self, password):
    self.password = pwd_context.hash(password)

  def verify_password(self, password):
    return pwd_context.verify(password, self.password)
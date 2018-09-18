"""
Database model files
"""

from . import db, bcrypt
from flask_login import UserMixin

class User(db.Document, UserMixin):
  email = db.StringField(require=True)
  password_hash = db.StringField(require=True)

  @staticmethod
  def create_with_password(email, password):
    password_hash = bcrypt.generate_password_hash(password)
    return User(email = email, password_hash = password_hash)

  def check_password(self, password):
    return bcrypt.check_password_hash(self.password_hash, password)

  def get_viewable_datasets(self):
    return Dataset.objects(owners__in = [self])

class Dataset(db.Document):
  name = db.StringField(require=True)
  owners = db.ListField(db.ReferenceField(User))
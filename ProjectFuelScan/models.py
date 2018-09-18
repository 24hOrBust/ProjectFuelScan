"""
Database model files
"""

from . import db, bcrypt
from flask_login import UserMixin
from mongoengine import Q

class User(db.Document, UserMixin):
  email = db.StringField(require=True)
  password_hash = db.StringField(require=True)
  can_create_datasets = db.BooleanField(default=False)

  @staticmethod
  def create_with_password(email, password):
    password_hash = bcrypt.generate_password_hash(password)
    return User(email = email, password_hash = password_hash)

  def check_password(self, password):
    return bcrypt.check_password_hash(self.password_hash, password)

  def get_viewable_datasets(self):
    return Dataset.objects( Q(owners = self) | Q(editors = self) | Q(viewers = self))

  def get_relationship_to_dataset(self, dataset):
    if self in dataset.owners:
      return 'Owner'
    if self in dataset.editors:
      return 'Editor'
    if self in dataset.viewer:
      return 'Viewer'

class Dataset(db.Document):
  name = db.StringField(require=True)
  owners = db.ListField(db.ReferenceField(User))
  editors = db.ListField(db.ReferenceField(User))
  viewers = db.ListField(db.ReferenceField(User))

  def is_owner(self, user):
    return user in self.owners
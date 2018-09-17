"""
Database model files
"""

from . import db

class User(db.Document):
  email = db.StringField(require=True)
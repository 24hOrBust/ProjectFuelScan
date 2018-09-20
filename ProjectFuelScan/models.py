"""
Database model files
"""

from . import db, bcrypt
from .geotagging import ImageMetaData
from flask_login import UserMixin
from mongoengine import Q
from datetime import datetime

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
    if self in dataset.viewers:
      return 'Viewer'

class Photograph(db.Document):
  created = db.DateTimeField()
  location = db.PointField()
  image = db.ImageField(thumbnail_size=(100, 100, True))

  @staticmethod
  def create_from_file(file):
    """
    Loads location and creation time metadata from a file like object.

    file:FileLike:a jpeg image with metadata
    """
    metadata = ImageMetaData(file)
    created = datetime.strptime(metadata.exif_data['DateTimeOriginal'], "%Y:%m:%d %H:%M:%S")
    lat_lng = metadata.get_lat_lng()
    file.seek(0)
    new_photo = Photograph(created = created, location = lat_lng)
    new_photo.image.put(file)
    
    return new_photo

class Dataset(db.Document):
  name = db.StringField(require=True)
  owners = db.ListField(db.ReferenceField(User), reverse_delete_rule = 'PULL')
  editors = db.ListField(db.ReferenceField(User), reverse_delete_rule = 'PULL')
  viewers = db.ListField(db.ReferenceField(User), reverse_delete_rule = 'PULL')
  photographs = db.ListField(db.ReferenceField(Photograph), reverse_delete_rule = 'PULL')

  def is_owner(self, user):
    return user in self.owners

  def is_editor(self, user):
    return (user in self.owners) or (user in self.editors)

  def is_viewer(self, user):
    return (user in self.owners) or (user in self.editors) or (user in self.viewers)
import pytest
import os

os.environ['UNIT_TESTING'] = "TRUE"

from ProjectFuelScan import app, db
from ProjectFuelScan.models import *

@pytest.fixture
def client():
  return app.test_client()

@pytest.fixture
def sample_data():
  with app.app_context():
    db.connection.drop_database(app.config['MONGODB_SETTINGS']['db'])
    bob = User(email="bob@example.com")
    bob.save()
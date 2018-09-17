import pytest

from ProjectFuelScan import app

@pytest.fixture
def client():
  return app.test_client()
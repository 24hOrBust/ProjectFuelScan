import pytest

from ProjectFuelScan import app

@pytest.fixture
def test_client():
  return app.test_client()
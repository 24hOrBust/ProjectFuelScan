from .fixtures import client

def test_home_reads_zero_users(client):
  rv = client.get('/')
  assert b'Their are 0 users' in rv.data
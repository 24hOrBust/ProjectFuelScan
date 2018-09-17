from .fixtures import client, sample_data

def test_home_reads_zero_users(client):
  rv = client.get('/')
  assert b'Their are 0 users' in rv.data

def test_home_reads_number_of_users(client, sample_data):
  rv = client.get('/')
  assert b'Their are 1 users' in rv.data
"""
Utility functions
"""

import os
import json

from urllib.parse import urlparse, urljoin
from flask import request, url_for

def get_mongodb_uri():
  raw_credentials = os.environ.get('VCAP_SERVICES') #Fetch ibm credentials

  if raw_credentials is None:
    #we are on a local development environment
    return 'mongodb://localhost:27017'

  #we are in the cloud, fetch the id
  credential = json.loads(raw_credentials)
  uri = credential['compose-for-mongodb'][0]['credentials']['uri']

  return uri

def load_config_from_env(app):
  """
  Fetches environment variables and loads them into `app` config

  app:Flask:the app to set the config on
  """
  app.config['MONGODB_SETTINGS'] = {
    'db':'project_fuel_scan',
    'host':get_mongodb_uri()
  }

  app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','dev key')

def is_safe_url(target):
  ref_url = urlparse(request.host_url)
  test_url = urlparse(urljoin(request.host_url, target))
  return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
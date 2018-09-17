"""
Utility functions
"""

import os
import json

def get_mongodb_uri():
  if os.environ.get('UNIT_TESTING'):
    #we are unit testing and want to connect to mongomock
    return 'mongomock://localhost'
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
    'db':os.environ.get('MONGO_DATABASE','project_fuel_scan'),
    'host':get_mongodb_uri()
  }
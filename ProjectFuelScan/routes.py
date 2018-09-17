"""
Web routes
"""

from . import app
from .models import *
from flask import request, render_template, g

@app.route('/')
def index():
  num_users = User.objects.count()
  return render_template('home.html', message = "Hello", num_users = num_users)
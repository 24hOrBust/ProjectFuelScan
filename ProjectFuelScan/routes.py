from . import app
from flask import request, render_template, g

@app.route('/')
def index():
  return render_template('home.html', message = "Hello")
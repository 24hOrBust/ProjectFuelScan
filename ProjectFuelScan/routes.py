"""
Web routes
"""

from . import app
from .models import *
from .forms import *
from .utils import is_safe_url
from flask import request, render_template, g, url_for, redirect, flash
from mongoengine import DoesNotExist
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
def index():
  num_users = User.objects.count()
  return render_template('home.html', message = "Hello", num_users = num_users)

@app.route('/login', methods=['GET','POST'])
def login():
  login_form = LoginForm()
  if login_form.validate_on_submit():
    try:
      user = User.objects.get(email = login_form.email.data)
      if not user.check_password(login_form.password.data):
        flash('Password incorrect')
        return render_template('login.html', form=login_form) 

      login_user(user)

      next = request.args.get('next')
      if not is_safe_url(next):
        return abort(400)

      return redirect(next or url_for('index'))

    except DoesNotExist:
      flash('Username incorrect')
      return render_template('login.html', form=login_form)
    
    return redirect(url_for('index'))

  return render_template('login.html', form = login_form)

@app.route('/logout')
@login_required
def logout():
  flash('Logged Out Successfully')
  logout_user()
  return redirect(url_for('index'))

@app.route('/datasets', methods=['GET','POST'])
@login_required
def datasets():
  form = CreateDatasetForm()
  print(type(current_user))

  if form.validate_on_submit():
    ds = Dataset( name = form.name.data, owners = [current_user.id] )
    ds.save()

  return render_template('datasets.html', datasets = current_user.get_viewable_datasets(), form=form)

@app.route('/datasets/<id>/delete', methods=['POST'])
@login_required
def delete_dataset(id):
  ds = Dataset.objects(id = id).get()
  if not ds.is_owner(current_user):
    abort(403)

  flash('Deleted dataset {name}'.format(name = ds.name))
  ds.delete()
  return redirect(url_for('datasets'))
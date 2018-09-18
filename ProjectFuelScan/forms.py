from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired

class LoginForm(FlaskForm):
  email = StringField( validators=[Email(), DataRequired()])
  password = PasswordField( validators=[DataRequired()])
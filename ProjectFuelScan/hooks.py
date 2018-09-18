from . import app, login_manager
from .models import User

@login_manager.user_loader
def load_user(user_id):
  return User.objects.get(id = user_id)


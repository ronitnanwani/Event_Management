from flask import Flask, render_template
from Event_Management.app.views import app_views,User
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

    
appf= Flask(__name__,template_folder='app/templates')
appf.secret_key = 'secret'  # Change this to something secure
# Login manager setup
login_manager = LoginManager()
login_manager.init_app(appf)
@login_manager.user_loader
# def load_user(user_id):
#     return User(user_id)
def load_user(email):
    print("load user",email)
    return User(email)
appf.register_blueprint(app_views)




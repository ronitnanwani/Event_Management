from flask import Flask, render_template
from Event_Management.app.views import app_views

appf= Flask(__name__,template_folder='app/templates')
appf.register_blueprint(app_views)



# import flask and template errors
from flask import Flask, render_template

# import a module or component using its Blueprint handler variable
from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_dashboard.controller import mod_dashboard as dashboard_module

# Define the WSGI application object
app = Flask(__name__)

# configurations
app.config.from_object('config')


# Error handler
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Register blueprint(s) ALL blueprints will be registered here
app.register_blueprint(auth_module)
app.register_blueprint(dashboard_module)

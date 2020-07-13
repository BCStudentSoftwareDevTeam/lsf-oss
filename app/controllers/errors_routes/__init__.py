from flask import render_template
from flask import Blueprint

error = Blueprint('errors_routes', __name__)


from app.controllers.errors_routes import handlers

from flask import Blueprint

error = Blueprint('errors_routes', __name__)

from app.errors_routes import handlers

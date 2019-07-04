from flask import Blueprint

bp = Blueprint('errors_routes', __name__)

from app.errors_routes import handlers

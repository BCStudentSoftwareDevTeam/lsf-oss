from flask import Blueprint
  
bp = Blueprint('main', __name__)

from app.main_routes import main_routes


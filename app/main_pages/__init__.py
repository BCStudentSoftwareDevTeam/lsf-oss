from flask import Blueprint
  
bp = Blueprint('main', __name__)

from app.main_pages import main_routes


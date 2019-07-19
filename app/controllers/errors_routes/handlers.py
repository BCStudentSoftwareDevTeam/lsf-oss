from flask import render_template
from app.controllers.errors_routes import error

@error.app_errorhandler(403)
def access_denied(error):
    return render_template('errors/403.html'), 403


@error.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@error.app_errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


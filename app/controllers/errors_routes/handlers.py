from flask import render_template, redirect, url_for
from app.controllers.errors_routes import error
from app import app


@error.app_errorhandler(403)
def access_denied(error):
    if app.config["USE_SHIBBOLETH"] == 0:
        return redirect(url_for("local_login.login"))
    return render_template('errors/403.html'), 403

@error.app_errorhandler(401)
def access_denied(error):
    if app.config["USE_SHIBBOLETH"] == 0:
        return redirect(url_for("local_login.login"))
    return render_template('errors/401.html'), 401


@error.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@error.app_errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

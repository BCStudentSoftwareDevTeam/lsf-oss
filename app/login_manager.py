from flask import request, session
from app import app, config
from app.controllers.errors_routes.handlers import *
from app.models.user import User, DoesNotExist
from app.logic.userInsertFunctions import createUser, createSupervisorFromTracy, createStudentFromTracy, InvalidUserException
from flask_login import current_user, logout_user


def require_login():
    env = request.environ
    username = getUsernameFromEnv(env)
    try:
        user = auth_user(env, username)
    except InvalidUserException as e:
        print("Invalid User:", e)
        raise
    if 'username' not in session:
        print("Logging in as", user)
        session['username'] = user
    return user


def getUsernameFromEnv(env):
    envK = "eppn"

    if app.config['USE_SHIBBOLETH'] and envK in env:
        username = env[envK].split("@")[0].split('/')[-1].lower()
        # print("Shib login", username)
        return username
    elif app.config['USE_SHIBBOLETH'] == 0:
        if not current_user.is_anonymous:
            return current_user.username
        return None
    else:
        print("Debug user!")
        return app.config['user']['debug']


def auth_user(env, username):
    """
    Ensure that the user has permission to access the application. If the user is permitted,
    ensure that a user entry is created in the user table from the Tracy data.
    """
    try:
        user = User.get(User.username == username)
        return user

    except DoesNotExist as e:
        """
        This exception cannot be tested naturally in development env because we cannot run Shibboleth,
        but the demo data is set up so that this exception should never happen inside of development env.
        """
        if app.config['USE_SHIBBOLETH']:
            description = env['description'].lower()
            supervisor = student = None
            if description == 'student':
                print("Adding {} to student table".format(username))
                student = createStudentFromTracy(username)
            else:
                print("Adding {} to supervisor table".format(username))
                supervisor = createSupervisorFromTracy(username)

            print("Creating record for {} in user table".format(username))
            return createUser(username, student=student, supervisor=supervisor)
        elif app.config['USE_SHIBBOLETH'] == 0:
            raise InvalidUserException

def logout():
    """
        Erases the session and returns the URL for redirection
    """
    if 'username' in session:
        print("Logging out", session['username'])
    session.clear()

    if app.config["USE_SHIBBOLETH"] == 0:
        logout_user()       # Call flask_login's logout handler
        url ="/login"   # url_for("local_login.login")
    if app.config['USE_SHIBBOLETH']:
        url = "/Shibboleth.sso/Logout"    
    return url

from flask import request
from app import cfg
from app.controllers.errors_routes.handlers import *
from app.models.user import User, DoesNotExist
from app.logic.userInsertFunctions import createUser, createSupervisorFromTracy, createStudentFromTracy, InvalidUserException

def getUsernameFromEnv(env):
    envK = "eppn"

    # Check if we are logging in via Shibboleth
    if envK in env:
        username = env[envK].split("@")[0].split('/')[-1].lower()
        return username
    else:
        return cfg['user']['debug']


def require_login():
    env = request.environ
    username = getUsernameFromEnv(env)

    try:
        user = auth_user(env, username)
    except InvalidUserException as e:
        print("Invalid User:", e)
        return False

    print("Logging in as", user.username)
    return user

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

from flask import request
from app import cfg
from app.controllers.errors_routes.handlers import *
from app.models.user import User, DoesNotExist
from app.logic.userInsertFunctions import createUserFromTracy, InvalidUserException

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

        try:
            user = Employee.get(Employee.username == username)
        except DoesNotExist as e:
            user = Student.get(Student.username == username)
        # user = User.get(User.username == username)
        return user

    except DoesNotExist as e:
        description = env['description'].lower()
        if description != 'student':
            print("Adding {} to employee table".format(username))
            return createEmployeeFromTracy(username)
        else:
            print("Adding {} to student table".format(username))
            return createStudentFromTracy(username)
            # raise InvalidUserException("Students must be added as administrators before logging in. {} is a student.".format(username))

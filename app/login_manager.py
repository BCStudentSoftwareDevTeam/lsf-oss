from flask import request
from app import cfg
from app.controllers.errors_routes.handlers import *
from app.models.user import User, DoesNotExist
from app.models.Tracy.stustaff import STUSTAFF

class InvalidUserException(Exception):
    pass

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
        description = env['description'].lower()
        if description != 'student':
            try:
                print("Adding {} to user table".format(username))

                # Get Tracy data
                #tracyUser = STUSTAFF.get(STUSTAFF.email="{}@berea.edu".format(username))
                #tracyUser = STUSTAFF.select().where(STUSTAFF.email="{}@berea.edu".format(username))
                tracyUser = STUSTAFF.get(EMAIL="{}@berea.edu".format(username))
                data = {
                    'PIDM': tracyUser.PIDM,
                    'username': username,
                    'FIRST_NAME': env['givenName'],
                    'LAST_NAME': env['sn'],
                    'ID': tracyUser.ID,
                    'EMAIL': env['eppn'],
                    'CPO': tracyUser.CPO,
                    'ORG': tracyUser.ORG,
                    'DEPT_NAME': tracyUser.DEPT_NAME,
                    'isLaborAdmin': False,
                    'isFinancialAidAdmin': False,
                    'isSaasAdmin': False,
                }
                user = User.create(**data)
                return user

            except DoesNotExist as e:
                raise InvalidUserException("{} not found in Tracy database".format(username))
            except Exception as e:
                raise InvalidUserException("Adding {} to user table failed".format(username), e)
        
        else:
            raise InvalidUserException("Students must be added as administrators before logging in.")

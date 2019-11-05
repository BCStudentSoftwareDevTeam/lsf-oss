from flask import request
from app import cfg
from app.controllers.errors_routes.handlers import *
from app.models.user import User


def getUsernameFromEnv():
    env = request.environ
    envK = "eppn"
    if envK in env:
        username = env[envK].split("@")[0].split('/')[-1].lower()
        add_user(env, username)
        return username
    else:
        print("Debug user!")
        return cfg['user']['debug']


def require_login():
    username = getUsernameFromEnv()
    print(username)

    try:
        user = User.get(User.username == username)
        print(user.username)
        return user
    except Exception as e:
        print(e)
        return False


def add_user(env, username):
    user = User.get(User.username == 1)
    if not user:
        description = request.environ['description'].lower()
        if description != 'student':
            try:
                newUser = User.insert(username, False, env['givenName'], env['sn'])
                return newUser
            except Exception as e:
                print(e)
                access_denied(403)
        else:
            not_found_error(404)

from app.logic.absolute_path import *
import yaml, os
import logging

def load_config(file):
    with open(file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    return cfg

def get_secret_cfg():
    secret_abs_path = getAbsolutePath('app/config','secret_config.yaml')
    secret_cfg      = load_config(secret_abs_path)
    return secret_cfg

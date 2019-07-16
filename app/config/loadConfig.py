'''
This script loads the yaml file, which holds all
configuration information.
'''
from app.logic.absolute_path import *
import yaml, os
import logging



def load_config(file):
    with open(file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    return cfg

# NOT DOCKER VERSION
def get_cfg():
    config_abs_path = getAbsolutePath('app/config/secret_config.yaml')
    cfg             = load_config(config_abs_path)
    return cfg

# DOCKER VERSION
#def get_cfg():
#    return load_config('app/config/config.yaml')

def get_secret_cfg():
    secret_abs_path = getAbsolutePath('app/config','secret.yaml')
    secret_cfg      = load_config(secret_abs_path)
    return secret_cfg

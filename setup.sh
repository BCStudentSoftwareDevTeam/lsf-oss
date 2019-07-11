#!/usr/bin/env bash
# Create the data directory if it doesn't exist
mkdir -p data

# Create a virtual machine virtual environment
if [ ! -d venv ]
then
  #virtualenv venv
  virtualenv --python=/usr/bin/python3 venv #Used this because source setup.sh was stuck on python 2
fi

. venv/bin/activate

# upgrade pip
python -m pip install --upgrade pip #added python-m for pip installs (source setu0p overwrite for venv)

python -m pip install -r requirements.txt

# Generate a new requirements.txt file by running "pip freeze > requirements.txt"





##install libraries needed for software
#
#pip install "flask"
## http://flask.pocoo.org/
#
#pip install "peewee"
## http://docs.peewee-orm.com/en/latest/
#
#pip install "flask-admin"
## # https://flask-admin.readthedocs.io/en/latest/
#
#pip install "wtf-peewee"
## # https://github.com/coleifer/wtf-peewee
#
#pip install "XlsxWriter"
#
## On MAC OSX, uninstall libyaml first and this succeeds: brew uninstall libyaml
#pip install "pyyaml"
#
#pip install "email_validator"
#
## pip install "pyDNS"
#
## Not needed, it's a client to use mysql, not the server itself
## pip install "MySQL-python"
#
##pip install "pymysql"
#
#pip install "flask_login"
#pip install git+https://github.com/memo330179/migrant-cli.git
#pip install --upgrade setuptools
#pip install flask-mysql
#pip install --upgrade pip enum34
#
#pip install git+https://github.com/mzdaniel/loadconfig
#
#pip install mysql-connector
#
#pip install flask-bootstrap
#
#pip install cryptography
#
#pip install peewee-migrations
#
##Fix me: ADD UPDATE_SCHEMA

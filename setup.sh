
# Establish variables for specific versions of libraries
FLASK_VERSION="${FLASK_VERSION:-0.12.2}"                  #0.12.2
PEEWEE_VERSION="${PEEWEE_VERSION:-2.10.1}"                #2.10.1
FLASK_ADMIN_VERSION="${FLASK_ADMIN_VERSION:-1.4.0}"       #1.4.0
WTF_PEEWEE_VERSION="${WTF_PEEWEE_VERSION:-0.2.6}"         #0.2.6
XLSXWRITER_VERSION="${XLSXWRITER_VERSION:-0.9.8}"         #0.9.8
PYAML_VERSION="${PYAML_VERSION:-3.12}"                    #3.12
EMAIL_VERSION="${EMAIL_VERSION:-1.0.2}"                   #1.0.2
MYSQLPYTHON_VERSION="${MYSQLPYTHON_VERSION=-1.2.5}"   #1.2.5
PYDNS="${PYDNS:-2.3.6}"                                   #2.3.6


# Create the data directory if it doesn't exist
mkdir -p data

# Create a virtual machine virtual environment
if [ ! -d venv ]
then
  virtualenv venv
fi

. venv/bin/activate

# upgrade pip
pip install --upgrade pip

#install libraries needed for software

pip install "flask"
# http://flask.pocoo.org/

pip install "peewee"
# http://docs.peewee-orm.com/en/latest/

pip install "flask-admin"
# # https://flask-admin.readthedocs.io/en/latest/

pip install "wtf-peewee"
# # https://github.com/coleifer/wtf-peewee

pip install "XlsxWriter"

# On MAC OSX, uninstall libyaml first and this succeeds: brew uninstall libyaml
pip install "pyyaml"

pip install "email_validator"

# pip install "pyDNS"

# Not needed, it's a client to use mysql, not the server itself
# pip install "MySQL-python"

#pip install "pymysql"

pip install "flask_login"
pip install git+https://github.com/memo330179/migrant-cli.git
pip install --upgrade setuptools
pip install flask-mysql
pip install --upgrade pip enum34

pip install git+https://github.com/mzdaniel/loadconfig

pip install mysql-connector

pip install flask-bootstrap

pip install cryptography

#Fix me: ADD UPDATE_SCHEMA 

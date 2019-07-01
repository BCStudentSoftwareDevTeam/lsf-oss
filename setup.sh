

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


# # Check for virtualenv
# command -v virtualenv >/dev/null 2>&1 || {
#     echo >&2 "setup.sh requires 'virtualenv' but it is not installed";
# }
#
# # Check for pip
# command -v pip3 >/dev/null 2>&1 || {
#  echo >&2 "source.sh requires 'pip' but it's not installed.";
# }

# Create the data directory if it doesn't exist
mkdir -p data

# Create a virtual machine virtual environment
if [ ! -d venv ]
then
  virtualenv venv
fi

. venv/bin/activate


# upgrade pip #Try sudo -H if it doesnt work
pip3 install --upgrade pip

#install libraries needed for software

pip3 install "flask==$FLASK_VERSION"
# http://flask.pocoo.org/

pip3 install "peewee==$PEEWEE_VERSION"
# http://docs.peewee-orm.com/en/latest/

pip3 install "flask-admin==$FLASK_ADMIN_VERSION"
# https://flask-admin.readthedocs.io/en/latest/

pip3 install "wtf-peewee==$WTF_PEEWEE_VERSION"
# https://github.com/coleifer/wtf-peewee

pip3 install "XlsxWriter==$XLSXWRITER_VERSION"

pip3 install "pyyaml==$PYAML_VERSION"

pip3 install "email_validator==$EMAIL_VERSION"

pip3 install "pyDNS==$PYDNS"

pip3 install "MySQL-python" #==$MYSQLPYTHON_VERSION"

pip3 install "pymysql"

pip3 install "flask-admin==$FLASK_ADMIN_VERSION"
pip3 install "wtf-peewee==$WTF_PEEWEE_VERSION"
pip3 install "flask_login==$FLASK_LOGIN_VERSION"
pip3 install git+https://github.com/memo330179/migrant-cli.git
pip3 install --upgrade setuptools
pip3 install flask-mysql
pip3 install --upgrade pip3 enum34

pip3 install git+https://github.com/mzdaniel/loadconfig

pip3 install mysql-connector
 ##FIX ME: ADD UPDATE_SCHEMA PLS ##

'''The purpose of this file is to setup the virtual environment
   In order to run the app you must use the command "source setup.sh"'''

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


# Check for virtualenv
command -v virtualenv >/dev/null 2>&1 || {
    echo >&2 "setup.sh requires 'virtualenv' but it is not installed";
    exit 1;
}

# Check for pip
command -v pip >/dev/null 2>&1 || {
 echo >&2 "source.sh requires 'pip' but it's not installed.";
 exit 1;
}

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

pip install "flask==$FLASK_VERSION"
# http://flask.pocoo.org/

pip install "peewee==$PEEWEE_VERSION"
# http://docs.peewee-orm.com/en/latest/

pip install "flask-admin==$FLASK_ADMIN_VERSION"
# https://flask-admin.readthedocs.io/en/latest/

pip install "wtf-peewee==$WTF_PEEWEE_VERSION"
# https://github.com/coleifer/wtf-peewee

pip install "XlsxWriter==$XLSXWRITER_VERSION"

pip install "pyyaml==$PYAML_VERSION"

pip install "email_validator==$EMAIL_VERSION"

pip install "pyDNS==$PYDNS"

pip install "MySQL-python" #==$MYSQLPYTHON_VERSION"

pip install "pymysql"

pip install "flask-admin==$FLASK_ADMIN_VERSION"
pip install "wtf-peewee==$WTF_PEEWEE_VERSION"
pip install "flask_login==$FLASK_LOGIN_VERSION"
pip install git+https://github.com/memo330179/migrant-cli.git
pip install --upgrade setuptools
pip install flask-mysql
pip install --upgrade pip enum34

pip install git+https://github.com/mzdaniel/loadconfig

pip install mysql-connector
 ##FIX ME: ADD UPDATE_SCHEMA PLS ##

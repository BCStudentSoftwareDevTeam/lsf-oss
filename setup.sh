'''
This file sets up the virtual environment.
Run "source setup.sh" each time you want to run the app.
'''
FLASK_VERSION="${FLASK_VERSION:-0.12.2}"              #0.12.2
PEEWEE_VERSION="${PEEWEE_VERSION:-2.10.2}"            #2.10.2
PYAML_VERSION="${PYAML_VERSION:-3.12}"                #3.12
XLSXWRITER_VERSION="${XLSXWRITER_VERSION:-1.0.2}"     #1.0.2
MYSQLPYTHON_VERSION="${MYSQLPYTHON_VERSION=-1.2.5}"   #1.2.5
FLASK_ADMIN_VERSION="${FLASK_ADMIN_VERSION:-1.5.0}"   #1.5.0
WTF_PEEWEE_VERSION="${WTF_PEEWEE_VERSION:-0.2.6}"     #0.2.6
FLASK_LOGIN_VERSION="${FLASK_LOGIN_VERSION:-0.4.1}"   #0.4.1


mkdir -p data

if [ ! -d venv ]
then
  virtualenv venv
fi

. venv/bin/activate

pip install "flask==$FLASK_VERSION"
pip install "peewee==$PEEWEE_VERSION"
pip install "pyyaml==$PYAML_VERSION"
pip install "XlsxWriter==$XLSXWRITER_VERSION"
# needed to migrate the cas.sql
pip install "MySQL-python" #==$MYSQLPYTHON_VERSION"
pip install "pymysql"
pip install "flask-admin==$FLASK_ADMIN_VERSION"
pip install "wtf-peewee==$WTF_PEEWEE_VERSION"
pip install "flask_login==$FLASK_LOGIN_VERSION"
pip install git+https://github.com/memo330179/migrant-cli.git
pip install --upgrade setuptools
pip install flask-mysql
pip install --upgrade pip enum34
pip install mysql-connector
# pip install libsqlite3-dev
##FIX ME: ADD UPDATE SCHEMA TO THIS FILE ##

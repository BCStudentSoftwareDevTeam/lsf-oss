#!/usr/bin/env bash

# Create a virtual machine virtual environment
if [ ! -d venv ]
then
  python3 -m venv venv
fi

. venv/bin/activate

# upgrade pip
python3 -m pip install --upgrade pip #added python-m for pip installs (source setup overwrite for venv)

python3 -m pip install -r requirements.txt

# To generate a new requirements.txt file, run "pip freeze > requirements.txt"

echo
if [[ ! -e app/config/secret_config.yaml ]]; then
	cp app/config/example_secret_config.yaml app/config/secret_config.yaml
	echo "Remember to edit your mail settings and MySQL connection information in 'app/config/secret_config.yaml'"
	echo
	echo "If your database has not been set up, you will need to run database/reset_database.sh"
fi

export PYTHON_VERSION=`python -c 'import sys; version=sys.version_info[:3]; print("{0}.{1}.{2}".format(*version))'`
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_RUN_PORT=8080

echo `python -c 'import sys; version=sys.version_info[:3]; print("{0}.{1}.{2}".format(*version))'`

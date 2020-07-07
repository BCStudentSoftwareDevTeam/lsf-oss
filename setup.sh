#!/usr/bin/env bash

# Check Python version number
if (("$((`python -c 'import sys; print(sys.version_info[0])'` >= 3))")); then
    if (("$((`python -c 'import sys; print(sys.version_info[1])'` >= 6))")); then
        echo "Python version meets system requirements (3.6 or newer)"
    else
        echo "Your version of Python is not up to date. Please update to Python 3.6 or newer"; return 1
    fi
else
    echo "Your version of Python is not up to date. Please update to Python 3.6 or newer"; return 1
fi


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

export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_RUN_PORT=8080

#!/usr/bin/env bash

# Remove any old virtual environments
rm -rf venv

# Capture the root password for MySQL
if [ -n "${rootpasswd+x}" ]; then 
        echo "WARNING: There is a MySQL root password stored in the environment!"; 
else 
        echo "Please enter root user MySQL password (Note: password will be hidden when typing):"
        read -s rootpasswd
fi

ls -al app/config/
# Install the database(s)
source db_install.sh

# Building secret_config.yaml
cp app/config/example_secret_config.yaml app/config/secret_config.yaml

# FIXME Tracy install if wanted:

# FIXME User Db install if wanted: 

# FIXME Banner install if wanted:


# Main db
printf ' host: "db" \n\n' | cat - app/config/secret_config.yaml > temp && mv temp app/config/secret_config.yaml
printf ' username: "%s" \n' $username | cat - app/config/secret_config.yaml > temp && mv temp app/config/secret_config.yaml
printf ' password: "%s" \n' $userpass | cat - app/config/secret_config.yaml > temp && mv temp app/config/secret_config.yaml
printf ' db_name: "%s" \n' $dbname | cat - app/config/secret_config.yaml > temp && mv temp app/config/secret_config.yaml
printf 'lsfdb: \n' | cat - app/config/secret_config.yaml > temp && mv temp app/config/secret_config.yaml

printf '# The local database for the application. This database must exist\n' | cat - app/config/secret_config.yaml > temp && mv temp app/config/secret_config.yaml
printf '################################### DATABASE CONNECTIONS ############################################################\n' | cat - app/config/secret_config.yaml > temp && mv temp app/config/secret_config.yaml


# Install all the Python libraries in a new venv
source setup.sh


# Create the tables
cd database
source reset_database.sh
cd ..



# Clear the root MySQL password from the environment
unset rootpasswd

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

# Building local_override.yaml
cp app/config/example_local_override.yaml app/config/local_override.yaml

# FIXME? Tracy install if wanted:

# FIXME? User Db install if wanted:

# FIXME? Banner install if wanted:


# Main db
printf ' host: "db" \n\n' | cat - app/config/local_override.yaml > temp && mv temp app/config/local_override.yaml
printf ' username: "%s" \n' $username | cat - app/config/local_override.yaml > temp && mv temp app/config/local_override.yaml
printf ' password: "%s" \n' $userpass | cat - app/config/local_override.yaml > temp && mv temp app/config/local_override.yaml
printf ' db_name: "%s" \n' $dbname | cat - app/config/local_override.yaml > temp && mv temp app/config/local_override.yaml
printf 'lsfdb: \n' | cat - app/config/local_override.yaml > temp && mv temp app/config/local_override.yaml

printf '# The local database for the application. This database must exist\n' | cat - app/config/local_override.yaml > temp && mv temp app/config/local_override.yaml
printf '################################### DATABASE CONNECTIONS ############################################################\n' | cat - app/config/local_override.yaml > temp && mv temp app/config/local_override.yaml


# Install all the Python libraries in a new venv
source setup.sh


# Create the tables
cd database
source reset_database.sh
cd ..


# Clear the root MySQL password from the environment
unset rootpasswd

#!/usr/bin/env bash

rm -rf venv

source setup.sh

if [ -n "${rootpasswd+x}" ]; then 
        echo "There is a MySQL root password stored in the environment"; 
else 
        echo "Please enter root user MySQL password (Note: password will be hidden when typing):"
        read -s rootpasswd
fi

source db_install.sh

cd database
source reset_database.sh
cd ..

unset rootpasswd

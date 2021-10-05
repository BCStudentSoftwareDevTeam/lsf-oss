#!/bin/bash
# Bash script written by Saad Ismail - me@saadismail.net
# Source: https://raw.githubusercontent.com/saadismail/useful-bash-scripts/master/db.sh


echo "Please enter the NAME of the new MySQL database! (example: database1)"
read dbname
charset="utf8"
echo "Creating new MySQL database..."
mysql -uroot -p${rootpasswd} -e "CREATE DATABASE ${dbname} /*\!40100 DEFAULT CHARACTER SET ${charset} */;"
echo "Database successfully created!"
echo "Showing existing databases..."
mysql -uroot -p${rootpasswd} -e "show databases;"
echo ""
echo "Please enter the NAME of the new MySQL database user! (example: user1)"
read username
echo "Please enter the PASSWORD for the new MySQL database user!"
echo "Note: password will be hidden when typing"
read -s userpass
echo "Creating new user..."
mysql -uroot -p${rootpasswd} -e "CREATE USER ${username}@localhost IDENTIFIED BY '${userpass}';"
echo "User successfully created!"
echo ""
echo "Granting ALL privileges on ${dbname} to ${username}!"
mysql -uroot -p${rootpasswd} -e "GRANT ALL PRIVILEGES ON ${dbname}.* TO '${username}'@'localhost';"
mysql -uroot -p${rootpasswd} -e "FLUSH PRIVILEGES;"

#!/bin/bash

if [ "`hostname`" == 'lsf.berea.edu' ]; then
	echo "DO NOT RUN THIS SCRIPT ON PRODUCTION UNLESS YOU REALLY REALLY KNOW WHAT YOU ARE DOING"
	exit 1
fi

echo "Dropping databases"
mysql -u root -proot --execute="DROP DATABASE \`lsf\`; DROP USER 'lsf_user';"
mysql -u root -proot --execute="DROP DATABASE \`UTE\`; DROP USER 'tracy_user';"

echo "Recreating databases and users"
mysql -u root -proot --execute="CREATE DATABASE IF NOT EXISTS \`lsf\`; CREATE USER IF NOT EXISTS 'lsf_user'@'%' IDENTIFIED BY 'password'; GRANT ALL PRIVILEGES ON *.* TO 'lsf_user'@'%';"
mysql -u root -proot --execute="CREATE DATABASE IF NOT EXISTS \`UTE\`; CREATE USER IF NOT EXISTS 'tracy_user'@'%' IDENTIFIED BY 'password'; GRANT ALL PRIVILEGES ON *.* TO 'tracy_user'@'%';"

rm -rf lsf_migrations
rm -rf tracy_migrations
rm -rf migrations.json

echo "Creating database schema"
./migrate_db.sh
./migrate_db_tracy.sh

rm -rf lsf_migrations
rm -rf tracy_migrations
rm -rf migrations.json

# Adding data we need in all environments
python3 base_data.py

# Adding fake data (we don't want this in a production environment)
python3 demo_data.py

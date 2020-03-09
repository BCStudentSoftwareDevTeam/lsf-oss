#!/bin/bash

mysql -u root --execute="DROP DATABASE \`lsf\`"
mysql -u root --execute="DROP DATABASE \`UTE\`"
mysql -u root --execute="CREATE DATABASE IF NOT EXISTS \`lsf\`; CREATE USER IF NOT EXISTS 'lsf_user'@'%' IDENTIFIED BY 'password'; GRANT ALL PRIVILEGES ON *.* TO 'lsf_user'@'%';"
mysql -u root --execute="CREATE DATABASE IF NOT EXISTS \`UTE\`; CREATE USER IF NOT EXISTS 'tracy_user'@'%' IDENTIFIED BY 'password'; GRANT ALL PRIVILEGES ON *.* TO 'tracy_user'@'%';"

./migrate_db.sh
./migrate_db_tracy.sh

# TODO only if we want to add fake data
python demo_data.py

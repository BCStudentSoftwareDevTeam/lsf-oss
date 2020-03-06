#!/bin/bash

mysql -u root -proot --execute="DROP DATABASE \`lsf\`"
mysql -u root -proot --execute="DROP DATABASE \`UTE\`"
mysql -u root -proot --execute="CREATE DATABASE IF NOT EXISTS \`lsf\`; CREATE USER 'lsf_user'@'%' IDENTIFIED BY 'password'; GRANT ALL PRIVILEGES ON *.* TO 'lsf_user'@'%';"
mysql -u root -proot --execute="CREATE DATABASE IF NOT EXISTS \`UTE\`; CREATE USER 'tracy_user'@'%' IDENTIFIED BY 'password'; GRANT ALL PRIVILEGES ON *.* TO 'tracy_user'@'%';"

./migrate_db.sh
./migrate_db_tracy.sh

# TODO only if we want to add fake data
python demo_data.py

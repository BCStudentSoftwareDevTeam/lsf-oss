# Installing MySQL

1. Download the latest version of MySQL from [https://www.mysql.com/downloads/] (MySQL's website). Alternatively, Ubuntu users can install MySQL server directly: ```sudo apt install mysql-server.```
2. Run the installer, following their instructions.

## Default username and password
By default, the mysql root user has no password and is only accessible when your host user is the superuser (root). This means that the command ```mysql -u root``` will not work out of the box as your normal user. You would need to use sudo, like ```sudo mysql -u root```. It is generally not good to have an unsecured root login anywhere, but if you are setting this up in a development environment it is probably ok. To change the user so you can access it without sudo, connect to mysql and run the following SQL:
```
mysql> DROP USER 'root'@'localhost';
mysql> CREATE USER 'root'@'%' IDENTIFIED BY '<PASS>';
mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
mysql> FLUSH PRIVILEGES;
```

Replace <PASS> with the password you want, or with nothing for an empty password.


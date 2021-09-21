# Flask application to manage Labor Status Forms

## Requirements
Python 3.6+ 
MySQL Server 8.0.6+
Ubuntu 20 (or other *nix systems that can run shell scripts)


**Required local packages (Ubuntu)**
 * python3-dev
 * python3-pip
 * python3-venv
 * unixodbc-dev

## Developing on Labor Status Forms
1. Pull down the repo: ```git clone <URL>```.
2. Run ```source setup.sh```.
3. Ensure mysql is running. You may need to do ```sudo systemctl start mysql```.
  3.a. (First time) Create an empty database. The default name is ```lsf```.
  3.b. (First time) Create another empty database. The default name is ```UTE```.
  3.c. (First time) Copy the file app/config/example_secret_config.yaml to app/config/secret_config.yaml.
  3.d. (First time) Edit app/config/secret_config.yaml to include the correct database names, and connecting username and password to access each databases above.
4. In the database directory, run ```./reset_database.sh```.
5. Run the app with ```flask run``` in the root directory.

## Using the Production database and real Tracy data
1. Set up your computer to access SQL Server databases (Instructions: http://ssdt-documentation.berea.edu/en/database).
2. Ensure your database connection is working by running ```python db_test.py```.
3. Check your secret_config.yml and make sure you have the necessary config items (check example_secret_config.yml)
4. Reset your database from the backup ```./reset_database.sh from-backup```.
5. Change your environment to ```staging```. Before starting the application, run ```export FLASK_ENV=staging```

## Updating pip dependencies (imports)
1. Anytime you add a Python dependency library, you'll need to run ```pip freeze > requirements.txt```. This file is used by **setup.sh** when the next user runs ```source setup.sh``` to ensure they have the correct Python dependencies.
NOTE: ```watchdog``` gets added by doing this step. Remove it after running the freeze command, as it breaks the setup.sh script

## Updating models
If the database schema needs to change, you must update the models. Follow the Peewee Migrator instructions to update models: https://pypi.org/project/peewee-migrations/

1. Install: ```pip install peewee-migrations``` (included in setup.sh, so you shouldn't need this)
2. ```pem init```
3. Add models to watch: e.g., ```pem add app.models.user.User```
4. Watch the model for changes: ```pem watch```
5. When done changing models, run the migrator to modify the db: ```pem migrate```

NOTE: You don't need to watch the files before you begin making changes.
The watch will compare the db to your model file and make any changes that are inconsistent.

Additional helpful commands:
- List active migrations: ```pem list```
- Show SQL generated by changes to the model: ```pem show```

- If encountering issues, try dropping your databases and adding them again. NOTE: This will remove any data in the database, so do NOT do this in a production environment.
- Delete any lsf/TRACY migrations files or folders. Note: ** Do NOT delete .JSON OR .SH files**

## Troubleshooting
1. If you can't clone the repository, make sure your SSH public key is added to your Github profile.
2. Make sure that you are running `source setup.sh` and `./reset\_database.sh`, in that order, without errors. Errors there should be resolved first.

## Email Configuration
There are a couple of options to test email handling. By default, all emails will be logged to the slack channel #labor-emails in the bereacs workspace.

If you want to test with actual emails, use an email other than outlook to test email handler. This setup is specific to gmail, but should work with any other email that allows you to make app passwords. These settings are stored in secret_config.yaml (example_secret_config.yaml if you haven't copied it yet). 

1. Set up two factor authentication on your Gmail (Security Settings)
2. Create an App Password through your Gmail. This 16 character password can only be viewed once, so make sure to save it. (NOTE: You won't have the option to create an app password unless step one is completed)
3. Inside of your secret_config.yaml file set the MAIL_USERNAME and MAIL_DEFAULT_SENDER as your Gmail, set the MAIL_PASSWORD as your new app password as, and set ALWAYS_SEND_MAIL as True. If you want emails to go to their real recipients, remove MAIL_OVERRIDE_ALL from your config or set it to "".
4. For testing purposes, change the email of the student and supervisor to match another email that can receive your test emails (or you can use MAIL_OVERRIDE_ALL to send everything to the address specified.

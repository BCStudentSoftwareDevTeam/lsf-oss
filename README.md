# Work Study Software System

## Code of Conduct

Before engaging with our community, you are expected to understand and abide by our [code of conduct](CODE_OF_CONDUCT.md). 

## Requirements

- Python 3.6+ 
- MySQL Server 8.0.6+
- Ubuntu 20 (or other *nix systems that can run shell scripts)
- Microsoft SQL Server (optional, for Tracy database)
- Oracle server (optional, for Banner database)

**Required local packages (Ubuntu)**
 * python3-dev
 * python3-pip
 * python3-venv
 * unixodbc-dev
 * libffi-dev

## Developers Guide

### Initial installation

NOTE: You must [install MySQL](INSTALL_MYSQL.md) and know the root password to continue. 

1. Pull down the repo: ```git clone <URL>```.
2. Ensure mysql is running. You may need to do ```sudo systemctl start mysql```.
   - (FIXME) Create another empty database. The default name is ```UTE```.
3. Edit ```app/config/default.yaml``` to match your application parameters.
4. Edit ```app/config/local_override.yaml``` for any local environment variables, such as username/passwords for the database. 
5. Run ```source install.sh```. 
6. Run the app with ```flask run``` in the root directory.

### Resetting the application during development

1. ```cd``` to the ```database``` directory. 
2. Run ```source reset_database.sh```.
3. Return to the root directory and run the app with ```flask run```. 

### Running tests against your new code
Test should be added in ```tests/code/```, logically grouped into files named ```test_EXAMPLE.py```. You can run tests individually with ```pytest```, or run the entire suite with ```tests/run_tests.sh```. The most common usage will be to run the non-ui tests continually by running ```tests/monitor.sh no-ui``` from the root directory of the repo. Where possible, use TDD and write your test before the code that makes it pass. Follow the Fail - Implement - Pass cycle.

### Updating pip dependencies (imports)
1. Anytime you add a Python dependency library, you'll need to run ```pip freeze > requirements.txt```. This file is used by **setup.sh** when the next user runs ```source setup.sh``` to ensure they have the correct Python dependencies.
NOTE: ```watchdog``` gets added by doing this step. Remove it after running the freeze command, as it breaks the setup.sh script

### Updating models

The application relies on a few databases: 

  - the main application database (required)
  - a Tracy database (required)
  - a Shibboleth database (or other authentication and authorization provider)
  - a Banner database (optional)

#### Main database changes

The main database uses MySQL as the database engine, and Peewee ORM to abstract the database in code. If the main database schema needs to change, you must update the models inside ```app/models```. Then, use Peewee Migrator to update the models in the MySQL database automagically: https://pypi.org/project/peewee-migrations/

1. Install: ```pip install peewee-migrations``` (included in the virtual environment on install, so you shouldn't need to do this)
2. ```pem init```
3. Add models to watch (e.g., ```pem add app.models.user.User```)
4. Watch the model for changes: ```pem watch```
5. When done changing models, run the migrator to modify the database: ```pem migrate```

NOTE: You don't need to watch the files before you begin making changes. The watch will compare the db to your model file and make any changes that are inconsistent.

**Additional helpful commands:**

- List active migrations: ```pem list```
- Show SQL generated by changes to the model: ```pem show```

- If encountering issues, try dropping your databases and adding them again. NOTE: This will remove any data in the database, so do NOT do this in a production environment.
- Delete any lsf/TRACY migrations files or folders. Note: ** Do NOT delete .JSON OR .SH files**

#### Tracy database changes

Unlike the main database, which uses MySQL, the Tracy database can use either MySQL (if you are installing the database yourself, i.e., ```USE_TRACY: 0``` in a config file) or Microsoft's SQL Server (if the database is being provided by the folks at Tracy, i.e., ```USE_TRACY: 1``` in a config file). To facilitate easier development, a Tracy class was created to access the database, regardless of the provider, leveraging SQAlchemy. It is recommended that any changes needed to the Tracy database are made to the models inside ```app/models/Tracy``` AND in the Tracy class inside ```app/logic/tracy.py```. 

NOTE: Peewee is used to abstract the main database, and SQAlchemy is used to abstract the Tracy database (regardless of the provider). 

#### Authentication and Authorization Provider

The application currently supports Shibboleth as the auth provider. To use it, set ```USE_SHIBBOLETH: 1``` in ```local_override.yaml```. If set to 0, a local auth provider will be used (i.e., Flask login). 

**FIXME:** Flask login is not yet implemented as a local provider.  

#### Banner Provider
Banner records are required at some institutions. To turn on this feature, set ```USE_BANNER: 1``` and provide the appropriate credentials in ```local_override.yaml```. 

### Email Configuration
There are a couple of options to test email handling. By default, all emails are suppressed by the flag ```USE_EMAILER: 0``` in ```default.yaml```. Setting this to 1 and providing credentials for an SMTP provider will enable emails to be sent. 

If you want to test with actual emails, use an email other than outlook to test the email handler. This setup is specific to Gmail, but should work with any other email that allows you to make app passwords. These settings are stored in ```default.yaml``` and can be overridden in ```local_override.yaml```. 

1. Set up two factor authentication on your Gmail (Security Settings).
2. Create an App Password through your Gmail. This 16 character password can only be viewed once, so make sure to save it. (NOTE: You won't have the option to create an app password unless step one is completed)
3. Inside of your ```local_override.yaml``` file set the MAIL_USERNAME and MAIL_DEFAULT_SENDER as your Gmail, set the MAIL_PASSWORD as your new app password, and set ```USE_EMAILER: 1```. If you want emails to go to their real recipients, remove MAIL_OVERRIDE_ALL from your config or set it to "".
4. For testing purposes, change the email of the student and supervisor to match another email that can receive your test emails (or you can use MAIL_OVERRIDE_ALL to send everything to the address specified.

### Using the Production database and real Tracy data (FIXME)

1. Set up your computer to access SQL Server databases (Instructions: http://ssdt-documentation.berea.edu/en/database).
2. Ensure your database connection is working by running ```python db_test.py```.
3. Check your production.yml and make sure you have the necessary credentials to connect to the servers.
4. Reset your database from the backup ```./reset_database.sh from-backup```.
5. Change your environment to ```staging```. Before starting the application, run ```export FLASK_ENV=staging``` (FIXME: should this be ```ENV=staging```?)

### Troubleshooting
1. If you can't clone the repository, make sure your SSH public key is added to your Github profile. HTTPS cloning is no longer allowed by Github.
2. The first time you are setting up the repository, run ```source install.sh```. 
3. As you make changes, run ```source setup.sh``` and ```./reset\_database.sh```, in that order, without errors. Errors there should be resolved first.

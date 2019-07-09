#pip install peewee==3.9.6
#pip install peewee-migrations==0.3.18

pem init
pem add app.models.Tracy.studata.STUDATA
pem add app.models.Tracy.stustaff.STUSTAFF
pem add app.models.Tracy.stuposn.STUPOSN
pem watch

pem migrate

#pip install peewee==3.9.6
#pip install peewee-migrations==0.3.18

pem init
pem add app.models.user.User
pem add app.models.laborStatusForm.LaborStatusForm
pem add app.models.laborReleaseForm.LaborReleaseForm
pem add app.models.term.Term

pem watch

pem migrate

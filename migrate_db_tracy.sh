#pip install peewee==3.9.6
#pip install peewee-migrations==0.3.18

pem init
pem add app.models.Tracy.studata.STUDATA
pem add app.models.Tracy.stustaff.STUSTAFF
pem add app.models.Tracy.stuposn.STUPOSN
pem add app.models.Tracy.term.Term
pem add app.models.Tracy.user.User
pem add app.models.Tracy.department.Department
pem add app.models.Tracy.emailTemplate.EmailTemplate
pem add app.models.Tracy.formHistory.formHistory
pem add app.models.Tracy.modifiedForm.modifiedForm
pem add app.models.Tracy.overloadForm.overloadForm
pem add app.models.Tracy.status.Status
pem add app.models.Tracy.student.Student
pem add app.models.Tracy.laborStatusForm.LaborStatusForm
pem add app.models.Tracy.laborReleaseForm.LaborReleaseForm
#what
pem watch

pem migrate

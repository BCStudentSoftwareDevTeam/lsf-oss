#pip install peewee==3.9.6
#pip install peewee-migrations==0.3.18

pem init
pem add app.models.user.User
pem add app.models.laborStatusForm.LaborStatusForm
pem add app.models.laborReleaseForm.LaborReleaseForm
pem add app.models.term.Term
pem add app.models.department.Department
pem add app.models.emailTemplate.EmailTemplate
# pem add app.models.formHistory.FormHistory
pem add app.models.modifiedForm.ModifiedForm
pem add app.models.overloadForm.OverloadForm
pem add app.models.status.Status
pem add app.models.student.Student

pem watch

pem migrate

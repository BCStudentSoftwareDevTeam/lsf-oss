from app.models import *

# For each modification made to an existing approved LSF, a new entry appears in this table
# Modifications to pending LSFs do not go on this table! The changes go directly to the LaborStatusForm table
class ModifiedForm(baseModel):
    modifiedFormID          = PrimaryKeyField()
    fieldModified           = CharField()
    oldValue                = CharField()
    newValue                = CharField()
    effectiveDate           = DateField()


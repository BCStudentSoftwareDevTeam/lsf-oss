from app.models.formHistory import FormHistory
from app.models.historyType import HistoryType
from app.models.status import Status
from app.models.adjustedForm import AdjustedForm
from app.models.laborStatusForm import LaborStatusForm
from app.models.overloadForm import OverloadForm
from app.models.adminNotes import AdminNotes
from app.models.user import User
from app.models.student import Student
from app.login_manager import require_login
from app.logic.tracy import Tracy
from app.logic.emailHandler import *
from datetime import date, datetime
from flask import flash
from flask import request


def modifyLSF(rsp, k, LSF, currentUser):
    if k == "supervisorNotes":
        LSF.supervisorNotes = rsp[k]["newValue"]
        LSF.save()

    if k == "supervisor":
        supervisor = createSupervisorFromTracy(bnumber=rsp[k]["newValue"])
        LSF.supervisor = supervisor.ID
        LSF.save()

    if k == "position":
        position = Tracy().getPositionFromCode(rsp[k]["newValue"])
        LSF.POSN_CODE = position.POSN_CODE
        LSF.POSN_TITLE = position.POSN_TITLE
        LSF.WLS = position.WLS
        LSF.save()

    if k == "weeklyHours":
        createOverloadForm(rsp, k, LSF, currentUser)
        LSF.weeklyHours = int(rsp[k]["newValue"])
        LSF.save()

    if k == "contractHours":
        LSF.contractHours = int(rsp[k]["newValue"])
        LSF.save()


def adjustLSF(rsp, k, LSF, currentUser):
    if k == "supervisorNotes":
        newNoteEntry = AdminNotes.create(formID        = LSF.laborStatusFormID,
                                         createdBy     = currentUser,
                                         date          = datetime.now().strftime("%Y-%m-%d"),
                                         notesContents = rsp[k]["newValue"])
        newNoteEntry.save()
    else:
        adjustedforms = AdjustedForm.create(fieldAdjusted = k,
                                            oldValue      = rsp[k]["oldValue"],
                                            newValue      = rsp[k]["newValue"],
                                            effectiveDate = datetime.strptime(rsp[k]["date"], "%m/%d/%Y").strftime("%Y-%m-%d"))
        historyType = HistoryType.get(HistoryType.historyTypeName == "Labor Adjustment Form")
        status = Status.get(Status.statusName == "Pending")
        formHistories = FormHistory.create(formID       = LSF.laborStatusFormID,
                                           historyType  = historyType.historyTypeName,
                                           adjustedForm = adjustedforms.adjustedFormID,
                                           createdBy    = currentUser,
                                           createdDate  = date.today(),
                                           status       = status.statusName)
        if k == "weeklyHours":
            createOverloadForm(rsp, k, LSF, adjustedforms.adjustedFormID, formHistories, currentUser)

def createOverloadForm(rsp, k, LSF, adjustedForm=None, formHistories=None, currentUser):
    allTermForms = LaborStatusForm.select() \
                   .join_from(LaborStatusForm, Student) \
                   .join_from(LaborStatusForm, FormHistory) \
                   .where((LaborStatusForm.termCode == LSF.termCode) & (LaborStatusForm.studentSupervisee.ID == LSF.studentSupervisee.ID) & (FormHistory.status != "Denied") & (FormHistory.historyType == "Labor Status Form"))
    previousTotalHours = 0
    if allTermForms:
        for statusForm in allTermForms:
            previousTotalHours += statusForm.weeklyHours

    if len(list(allTermForms)) == 1:
        newTotalHours = int(rsp[k]['newValue'])
    else:
        newTotalHours = previousTotalHours + int(rsp[k]['newValue'])

    if previousTotalHours <= 15 and newTotalHours > 15:
        newLaborOverloadForm = OverloadForm.create(studentOverloadReason = "None")
        newFormHistory = FormHistory.create(formID       = LSF.laborStatusFormID,
                                            historyType  = "Labor Overload Form",
                                            createdBy    = currentUser,
                                            adjustedForm = adjustedForm,
                                            overloadForm = newLaborOverloadForm.overloadFormID,
                                            createdDate  = date.today(),
                                            status       = "Pending")
        try:
            if formHistories:
                overloadEmail = emailHandler(formHistories.formHistoryID)
            else:
                overloadEmail = emailHandler(newFormHistory.formHistoryID)
            overloadEmail.LaborOverLoadFormSubmitted("http://{0}/".format(request.host) + "studentOverloadApp/" + str(newFormHistory.formHistoryID))
        except Exception as e:
            print("An error occured while attempting to send overload form emails: ", e)

    # This will delete an overload form after the hours are changed
    elif previousTotalHours > 15 and int(rsp[k]['newValue']) <= 15:
        deleteOverloadForm = FormHistory.get((FormHistory.formID == LSF.laborStatusFormID) & (FormHistory.historyType == "Labor Overload Form"))
        deleteOverloadForm = OverloadForm.get(OverloadForm.overloadFormID == deleteOverloadForm.overloadForm.overloadFormID)
        deleteOverloadForm.delete_instance()

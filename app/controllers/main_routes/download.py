from flask import flash
from app.models.laborStatusForm import LaborStatusForm
from app.models.formHistory import *
import csv
from app.controllers.main_routes.main_routes import *
from app.models.supervisor import Supervisor
from app.logic.tracy import Tracy

class ExcelMaker:
    '''
    Create the excel for the download bottons
    '''
    def __init__(self):

        form = LaborStatusForm.select()
        studentForm = []

    ## get all the labor status forms with the form id passed in from python controller ##
    def makeExcelStudentHistory(self, formid):
        downloadForms = []
        for id in formid:
            studentForms = LaborStatusForm.select().where(LaborStatusForm.laborStatusFormID == id)
            for studentForm in studentForms:
                downloadForms.append(studentForm)

        with open('app/static/files/LaborStudent.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

        ## Create heading on csv ##
            filewriter.writerow(['Name',
                                'B#',
                                'Term',
                                'Department',
                                'Supervisor',
                                'Position',
                                'Labor Position Title',
                                'Labor Position Code',
                                'WLS',
                                'Weekly Hours',
                                'Total Contract Hours',
                                'Start Date',
                                'End Date',
                                'Supervisor Notes'])
        ## fill infomations ##
            for form in downloadForms:
                filewriter.writerow([form.studentSupervisee.FIRST_NAME + " " + form.studentSupervisee.LAST_NAME,
                                    form.studentSupervisee.ID,
                                    form.termCode.termName,
                                    form.department.DEPT_NAME,
                                    form.supervisor.FIRST_NAME + " " + form.supervisor.LAST_NAME,
                                    form.jobType,
                                    form.POSN_TITLE,
                                    form.POSN_CODE,
                                    form.WLS,
                                    form.weeklyHours,
                                    form.contractHours,
                                    form.startDate,
                                    form.endDate,
                                    form.supervisorNotes])
        return 'static/files/LaborStudent.csv';

    def makeExcelAllPendingForms(self, pendingForms):
        with open('app/static/files/LaborStudent.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
        ## Create heading on csv ##
            filewriter.writerow(['Name',
                                'B#',
                                'Labor Position Title',
                                'Labor Position Code',
                                'Supervisor',
                                'Department',
                                'WLS',
                                'Weekly Hours',
                                'Total Contract Hours',
                                'Term',
                                'Start Date',
                                'End Date',
                                'Position',
                                'Supervisor Notes'])
        ## fill infomations ##
            for form in pendingForms:
                weeklyHours = form.formID.weeklyHours
                contractHours = form.formID.contractHours
                supervisor = form.formID.supervisor.FIRST_NAME + " " + form.formID.supervisor.LAST_NAME
                position = form.formID.POSN_TITLE
                positionCode = form.formID.POSN_CODE
                positionWLS = form.formID.WLS

                if form.historyType.historyTypeName == "Labor Adjustment Form":
                    if form.adjustedForm.fieldAdjusted == "weeklyHours":
                        weeklyHours = form.adjustedForm.newValue
                    if form.adjustedForm.fieldAdjusted == "contractHours":
                        contractHours = form.adjustedForm.newValue
                    if form.adjustedForm.fieldAdjusted == "supervisor":
                        newSupervisorID = form.adjustedForm.newValue
                        newSupervisor = Supervisor.get(Supervisor.ID == newSupervisorID)
                        supervisor = newSupervisor.FIRST_NAME +" "+ newSupervisor.LAST_NAME
                    if form.adjustedForm.fieldAdjusted == "position":
                        newPositionCode = form.adjustedForm.newValue
                        newPosition = Tracy().getPositionFromCode(newPositionCode)
                        position = newPosition.POSN_TITLE
                        positionCode = newPosition.POSN_CODE
                        positionWLS = newPosition.WLS

                filewriter.writerow([form.formID.studentSupervisee.FIRST_NAME + " " + form.formID.studentSupervisee.LAST_NAME,
                                    form.formID.studentSupervisee.ID,
                                    position,
                                    positionCode,
                                    supervisor,
                                    form.formID.department.DEPT_NAME,
                                    positionWLS,
                                    weeklyHours,
                                    contractHours,
                                    form.formID.termCode.termName,
                                    form.formID.startDate,
                                    form.formID.endDate,
                                    form.formID.jobType,
                                    form.formID.supervisorNotes])
        return 'static/files/LaborStudent.csv';

    def makeList(self, student):
        downloadForms = []
        for id in student:
            studentForm = LaborStatusForm.select().where(LaborStatusForm.laborStatusFormID == id)
            for studentF in studentForm:
                downloadForms.append(studentF)

        with open('app/static/files/LaborStudent.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

        ## Create heading on csv ##
            filewriter.writerow(['Name',
                                'B#',
                                'Labor Position Title',
                                'Labor Position Code',
                                'Supervisor',
                                'Department',
                                'WLS',
                                'Weekly Hours',
                                'Total Contract Hours',
                                'Term',
                                'Start Date',
                                'End Date',
                                'Position',
                                'Supervisor Notes'])
        ## fill infomations ##
            for form in downloadForms:
                filewriter.writerow([form.studentSupervisee.FIRST_NAME + " " + form.studentSupervisee.LAST_NAME,
                                    form.studentSupervisee.ID,
                                    form.POSN_TITLE,
                                    form.POSN_CODE,
                                    form.supervisor.FIRST_NAME + " " + form.supervisor.LAST_NAME,
                                    form.department.DEPT_NAME,
                                    form.WLS,
                                    form.weeklyHours,
                                    form.contractHours,
                                    form.termCode.termName,
                                    form.startDate,
                                    form.endDate,
                                    form.jobType,
                                    form.supervisorNotes])
        return 'static/files/LaborStudent.csv';

def main():
    ExcelMaker()

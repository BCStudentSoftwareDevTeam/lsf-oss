from flask import flash
from app.models.laborStatusForm import LaborStatusForm
from app.models.Tracy.studata import STUDATA
import csv
from app.controllers.main_routes.main_routes import *

class ExcelMaker:
    '''
    Create the excel for the download bottons
    '''
    def __init__(self):

        form = LaborStatusForm.select()
        studentForm = []

    ## get all the labor status forms with the form id passed in from python controller ##
    def makeList(self, student):
        downloadForms = []
        for id in student:
            studentForm = LaborStatusForm.select().where(LaborStatusForm.laborStatusFormID == id)
            for studentF in studentForm:
                downloadForms.append(studentF)
            print(id)


        with open('app/static/LaborStudent.csv', 'w') as csvfile:
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
                                'Contract Hours',
                                'Term',
                                'Start Date',
                                'End Date',
                                'Position',
                                'Supervisor Notes'])
        ## fill infomations ##
            for form in downloadForms:
                print(form.POSN_TITLE)
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


        return 'static/LaborStudent.csv';


def main():
    ExcelMaker()

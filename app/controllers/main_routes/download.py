from flask import flash
from app.models.laborStatusForm import LaborStatusForm
from app.models.Tracy.studata import STUDATA
import csv
from app.controllers.main_routes.main_routes import *

class ExcelMaker:
    def __init__(self):

        form = LaborStatusForm.select()
        studentForm = []

    def makeList(self, student):
        a = []
        for i in student:
            print(i)
            studentForm = LaborStatusForm.select().where(LaborStatusForm.laborStatusFormID == i)
            for studentF in studentForm:
                a.append(studentF)
        print(a)
        for i in a:
            print(i.POSN_TITLE)

        print("i")
        #print(student)
        with open('app/static/LaborStudent.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            #print(student)
            filewriter.writerow(['Name', 'B#', 'Title', 'Supervisor', 'Department', 'WLS', 'Hours', 'Term', 'Position', 'Supervisor Notes', 'Admin Notes'])
            for i in a:

                filewriter.writerow([i.studentSupervisee.FIRST_NAME + " " + i.studentSupervisee.LAST_NAME,
                                    i.studentSupervisee.ID,
                                    i.POSN_TITLE,
                                    i.supervisor.FIRST_NAME + " " + i.supervisor.LAST_NAME,
                                    i.department.DEPT_NAME,
                                    i.WLS,
                                    i.weeklyHours,
                                    i.termCode.termName,
                                    i.jobType,
                                    i.supervisorNotes,
                                    i.laborDepartmentNotes])





def main():
    ExcelMaker()

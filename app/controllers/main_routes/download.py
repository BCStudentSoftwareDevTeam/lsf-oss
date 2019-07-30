from flask import flash
from app.models.laborStatusForm import LaborStatusForm
from app.models.Tracy.studata import STUDATA
import csv
from app.controllers.main_routes.main_routes import *

class ExcelMaker:
    def __init__(self, student):
        student = student
        self.ID = self
        self.makeList(student)
    def makeList(self, student):
        print("i")
        print(student)
        with open('app/static/LaborStudent.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            #print(student)
            filewriter.writerow(['Name', 'B#','Date',student, 'apple'])


def main():
    ExcelMaker()

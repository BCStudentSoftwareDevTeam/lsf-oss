import csv
from app import app
app.config['ENV'] = 'production'

from app.logic.userInsertFunctions import *
from app.logic.tracy import Tracy
from app.models.term import Term
from app.models.laborStatusForm import LaborStatusForm
from app.models.department import Department
from app.controllers.admin_routes.termManagement import createTerms


def get_reader(f, fields):
    reader = csv.DictReader(f, delimiter=',', fieldnames=fields, restkey='extra', restval='XXXX')
    reader.__next__() # skip header

    return reader

def get_list(f, fields):
    reader = get_reader(f, fields)
    return [row for row in reader]

def validate_file(f, fields):
    reader = get_reader(f, fields)
    success = True

    # Check for places where we didn't escape text
    for row in reader:
        if 'extra' in row and row['extra'] is not None:
            print("{}:".format(reader.line_num), "Extra comma in line. Need quotes")
            success = False

        try:
            int(row['form_id'])
            if row['note'] == 'XXXX':
                print("{}:".format(reader.line_num), "Not enough columns")
                success = False
        except:
            print("{}:".format(reader.line_num), "Bad ID '{}'. Need quotes on previous line.".format(row['form_id']))
            success = False
            
    f.seek(0)

    return success


# past forms
fields = ['form_id', # internal id
        'primarySupervisor', # bnumber, only has a value sometimes
        'PrimarySupervisorName', # text, only has a value sometimes
        'created_on', # null at the beginning, then datetime string with ms
        'jobType', # Primary, Secondary, Secondary (Break Labor)
        'supervisee', # student bnumber
        'superviseeName', # student name
        'supervisor', # staff bnumber
        'supervisorName', # staff name
        'creator', # username
        'term', # term title
        'posnCode', # position code
        'positionName', # position name
        'hour', # contract hours (only a per-day value. grrr) or weekly hours
        'WLS', # WLS number
        'start', # contract start
        'end', # contract end
        'approval', # 1 for approved, -1 for rejected, empty for pending?
        'rejectReason', # text for rejection
        'department', # department text
        'departmentCode', # department #
        'processedBy', # username
        'processedDate', # datetime string with ms
        'departmentAccount', # number. what's the difference between this and department code?
        'note' # text note
        ]
with open('old-data/short-pastLSF.txt','r',encoding="cp1252",newline='') as pastLSF:
    if validate_file(pastLSF, fields):
        createTerms(2015)
        createTerms(2016)
        createTerms(2017)
        createTerms(2018)
        createTerms(2019)
        createTerms(2020)

        data = get_list(pastLSF, fields)
        for record in data:
            print(record)

            save = True

            # Populate department table
            department = Department.get_or_create(
                DEPT_NAME=record['department'],
                ACCOUNT=record['departmentAccount'],
                ORG=record['departmentCode'])

            # We don't have to store this here in the new db model
            #if record['primarySupervisor']:
            #    createSupervisorFromTracy(bnumber=record['primarySupervisor'])
            
            # Ensure Supervisor record exists
            try:
                supervisor = createSupervisorFromTracy(bnumber=record['supervisor'])
                print("Found {} as a supervisor".format(supervisor.FIRST_NAME + " " + supervisor.LAST_NAME))
            except InvalidUserException:
                print("Can't find a matching supervisor for {}".format(record['supervisor']))
                save = False
                # We have to create a supervisor, but we don't have their data from Tracy, just name and bnumber

            # Ensure Student record exists
            try:
                obj = Tracy().getStudentFromBNumber(record['supervisee'])
                student = createStudentFromTracy(obj)
                print("Found {} as a student".format(student.FIRST_NAME + " " + student.LAST_NAME))
            except InvalidQueryException:
                print("Can't find a matching student for {}".format(record['supervisee']))
                save = False
            except InvalidUserException:
                print("Couldn't create a student for {}".format(record['supervisee']))
                save = False

            try:
                term = Term.get(Term.termName == record['term'].strip())
            except:
                print("Can't find a matching term for {}".format(record['term']))
                save = False

            if save:

                weekly_hours = record['hour']
                contract_hours = None
                if term.isBreak:
                    weekly_hours = None
                    contract_hours = int(record['hour']) * 5 # we need a total, but that's hard. here's a week

                if term.isSummer:
                    contract_hours *= 8 # how many weeks is summer?

                form = LaborStatusForm.create({
                    'studentName': record['superviseeName'],
                    'termCode': term.termCode,
                    'studentSupervisee': student,
                    'supervisor': supervisor,
                    'department': department,
                    'jobType': 'Primary' if record['jobType'] == 'Primary' else 'Secondary',
                    'WLS': record['WLS'],
                    'POSN_TITLE': record['positionName'],
                    'POSN_CODE': record['posnCode'],
                    'contractHours': contract_hours,
                    'weeklyHours': weekly_hours,
                    'startDate': record['start'],
                    'endDate': record['end'],
                    'laborDepartmentNotes': record['note']})

                print("Saved.")
            else:
                print("XX Not saved XX")

exit()

# Current forms
fields = ['primarySupervisor', # bnumber. only has a value sometimes
        'created_on', # datetime string with ms
        'jobType', # Primary or Secondary
        'supervisee', # student bnumber
        'supervisor', # staff bnumber
        'creator', # username
        'term', # term title
        'posn_code', # position code
        'hour', # hours (contract or weekly)
        'form_id', # internal ID
        'start', # contract start
        'end', # contract end
        'note' # text note
        ]
with open('old-data/lsf.txt','r',encoding="cp1252",newline='') as forms:
    if validate_file(forms, fields):
        data = get_list(forms, fields)
        print(data)

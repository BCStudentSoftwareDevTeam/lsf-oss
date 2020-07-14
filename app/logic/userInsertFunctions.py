from flask_login import login_required
from app.controllers.main_routes import *
from app.models.user import *
from app.models.status import *
from app.models.laborStatusForm import *
from app.models.overloadForm import *
from app.models.formHistory import*
from app.models.historyType import *
from app.models.term import *
from app.models.student import Student
from app.models.supervisor import Supervisor
from app.models.department import *
from flask import json, jsonify
from flask import request
from datetime import datetime, date
from flask import Flask, redirect, url_for, flash
from app import cfg
from app.logic.emailHandler import emailHandler
from app.logic.tracy import Tracy, InvalidQueryException
from peewee import DoesNotExist

class InvalidUserException(Exception):
    pass

def createUser(username, student=None, supervisor=None):
    """
    Retrieves or creates a user in the User table and updates Supervisor and/or Student as requested.

    Raises InvalidUserException if this does not succeed.
    """

    if not student and not supervisor:
        raise InvalidUserException("A User should be connected to Student or Supervisor")

    try:
        user = User.get_or_create(username=username)[0]

    except Exception as e:
        raise InvalidUserException("Adding {} to user table failed".format(username), e)

    if student:
        user.Student = student.ID # Not sure why assigning the object doesn't work...
    if supervisor:
        user.Supervisor = supervisor.ID

    user.save()

    return user


def createSupervisorFromTracy(username):
    """
        Attempts to add a user from the Tracy database to the application, based on the provided username.
        XXX Currently only handles adding staff. XXX

        Raises InvalidUserException if this does not succeed.
    """

    email = "{}@berea.edu".format(username)
    try:
        tracyUser = Tracy().getSupervisorFromEmail(email)
    except DoesNotExist as e:
        raise InvalidUserException("{} not found in Tracy database".format(email))

    try:
        return Supervisor.get_or_create(PIDM = tracyUser.PIDM,
                                        FIRST_NAME = tracyUser.FIRST_NAME,
                                        LAST_NAME = tracyUser.LAST_NAME,
                                        ID = tracyUser.ID.strip(),
                                        EMAIL = email,
                                        CPO = tracyUser.CPO,
                                        ORG = tracyUser.ORG,
                                        DEPT_NAME = tracyUser.DEPT_NAME)[0]
    except Exception as e:
        raise InvalidUserException("Adding {} to Supervisor table failed".format(username), e)

def createStudentFromTracy(username):
    """
        Checks to see if username of student is in Tracy database, based on the provided username.

        Raises InvalidUserException if this does not succeed.
    """
    email = "{}@berea.edu".format(username)
    try:
        tracyStudent = Tracy().getStudentFromEmail(email)
    except DoesNotExist as e:
        raise InvalidUserException("{} not found in Tracy database".format(email))

    return createStudentFromTracyObj(tracyStudent)

def createStudentFromTracyObj(tracyStudent):
    """
        Attempts to add a student from the Tracy database to the application, based on the provided object from the Tracy student database.

        Raises InvalidUserException if this does not succeed.
    """
    try:
        return Student.get_or_create(ID = tracyStudent.ID.strip(),
                                    PIDM = tracyStudent.PIDM,
                                    FIRST_NAME = tracyStudent.FIRST_NAME,
                                    LAST_NAME = tracyStudent.LAST_NAME,
                                    CLASS_LEVEL = tracyStudent.CLASS_LEVEL,
                                    ACADEMIC_FOCUS = tracyStudent.ACADEMIC_FOCUS,
                                    MAJOR = tracyStudent.MAJOR,
                                    PROBATION = tracyStudent.PROBATION,
                                    ADVISOR = tracyStudent.ADVISOR,
                                    STU_EMAIL = tracyStudent.STU_EMAIL,
                                    STU_CPO = tracyStudent.STU_CPO,
                                    LAST_POSN = tracyStudent.LAST_POSN,
                                    LAST_SUP_PIDM = tracyStudent.LAST_SUP_PIDM)[0]
    except Exception as e:
        raise InvalidUserException("Adding {} to user table failed".format(username), e)


def createLaborStatusForm(tracyStudent, studentID, primarySupervisor, department, term, rspFunctional):
    """
    Creates a labor status form with the appropriate data passed from userInsert() in laborStatusForm.py
    tracyStudent: object with all the student's information from Tracy
    studentID: student's primary ID in the database AKA their B#
    primarySupervisor: primary supervisor of the student
    department: department the position is a part of
    term: term when the position will happen
    rspFunctional: a dictionary containing all the data submitted in the LSF page
    returns the laborStatusForm object just created for later use in laborStatusForm.py
    """
    # Changes the dates into the appropriate format for the table
    startDate = datetime.strptime(rspFunctional['stuStartDate'], "%m/%d/%Y").strftime('%Y-%m-%d')
    endDate = datetime.strptime(rspFunctional['stuEndDate'], "%m/%d/%Y").strftime('%Y-%m-%d')
    # Creates the labor Status form
    lsf = LaborStatusForm.create(termCode_id = term,
                                 studentSupervisee_id = studentID,
                                 supervisor_id = primarySupervisor,
                                 department_id  = department,
                                 jobType = rspFunctional["stuJobType"],
                                 WLS = rspFunctional["stuWLS"],
                                 POSN_TITLE = rspFunctional["stuPosition"],
                                 POSN_CODE = rspFunctional["stuPositionCode"],
                                 contractHours = rspFunctional.get("stuContractHours", None),
                                 weeklyHours   = rspFunctional.get("stuWeeklyHours", None),
                                 startDate = startDate,
                                 endDate = endDate,
                                 supervisorNotes = rspFunctional["stuNotes"],
                                 laborDepartmentNotes = rspFunctional["stuLaborNotes"],
                                 studentName = rspFunctional["stuName"]
                                 )

    return lsf


def createOverloadFormAndFormHistory(rspFunctional, lsf, creatorID, status):
    """
    Creates a 'Labor Status Form' and then if the request needs an overload we create
    a 'Labor Overload Form'. Emails are sent based on whether the form is an 'Overload Form'
    rspFunctional: a dictionary containing all the data submitted in the LSF page
    lsf: stores the new instance of a labor status form
    creatorID: id of the user submitting the labor status form
    status: status of the labor status form (e.g. Pending, etc.)
    """
    # We create a 'Labor Status Form' first, then we check to see if a 'Labor Overload Form'
    # needs to be created
    historyType = HistoryType.get(HistoryType.historyTypeName == "Labor Status Form")
    FormHistory.create( formID = lsf.laborStatusFormID,
                        historyType = historyType.historyTypeName,
                        overloadForm = None,
                        createdBy   = creatorID,
                        createdDate = date.today(),
                            status      = status.statusName)
    if rspFunctional.get("isItOverloadForm") == "True":
        overloadHistoryType = HistoryType.get(HistoryType.historyTypeName == "Labor Overload Form")
        newLaborOverloadForm = OverloadForm.create( studentOverloadReason = None,
                                                    financialAidApproved = None,
                                                    financialAidApprover = None,
                                                    financialAidReviewDate = None,
                                                    SAASApproved = None,
                                                    SAASApprover = None,
                                                    SAASReviewDate = None,
                                                    laborApproved = None,
                                                    laborApprover = None,
                                                    laborReviewDate = None)
        formOverload = FormHistory.create( formID = lsf.laborStatusFormID,
                                            historyType = overloadHistoryType.historyTypeName,
                                            overloadForm = newLaborOverloadForm.overloadFormID,
                                            createdBy   = creatorID,
                                            createdDate = date.today(),
                                            status      = status.statusName)
        email = emailHandler(formOverload.formHistoryID)
        email.LaborOverLoadFormSubmitted('http://{0}/'.format(request.host) + 'studentOverloadApp/' + str(formOverload.formHistoryID))
    else:
        email = emailHandler(FormHistory.formHistoryID)
        email.laborStatusFormSubmitted()

def emailDuringBreak(secondLSFBreak, term):
    """
    Sending emails during break period
    """
    if term.isBreak:
        isOneLSF = json.loads(secondLSFBreak)
        formHistory = FormHistory.get(FormHistory.formHistoryID == isOneLSF['formHistoryID'])
        if(isOneLSF["isMoreLSf"] == True): #Student has more than one lsf. Send email to both supervisors and student
            for lsfID in isOneLSF["lsfFormID"]: # send email per previous lsf form
                email = emailHandler(formHistory.formHistoryID, lsfID)
                email.notifySecondLaborStatusFormSubmittedForBreak()
        else: # Student has only one lsf, send email to student and supervisor
            email = emailHandler(formHistory.formHistoryID)
            email.laborStatusFormSubmittedForBreak()

def checkForSecondLSFBreak(termCode, student):
    """
    Checks if a student has more than one labor status form submitted for them during a break term, and sends emails accordingly.
    """
    positions = LaborStatusForm.select().where(LaborStatusForm.termCode == termCode, LaborStatusForm.studentSupervisee == student)
    isMoreLSF_dict = {}
    storeLsfFormsID = []
    previousSupervisorNames = []
    if len(list(positions)) >= 1: # If student has one or more than one lsf
        isMoreLSF_dict["ShowModal"] = True # show modal when the student has one or more than one lsf

        for item in positions:
            previousSupervisorNames.append(item.supervisor.FIRST_NAME + " " + item.supervisor.LAST_NAME)
            isMoreLSF_dict["studentName"] = item.studentSupervisee.FIRST_NAME + " " + item.studentSupervisee.LAST_NAME
        isMoreLSF_dict['primarySupervisorNames'] = previousSupervisorNames

        if len(list(positions)) == 1: # if there is only one labor status form then send email to the supervisor and student
            laborStatusFormID = positions[0].laborStatusFormID
            formHistoryID = FormHistory.get(FormHistory.formID == laborStatusFormID)
            isMoreLSF_dict["isMoreLSf"] = False
            isMoreLSF_dict["formHistoryID"] = formHistoryID.formHistoryID

        else: # if there are more lsfs then send email to student, supervisor and all previous supervisors
            isMoreLSF_dict["isMoreLSf"] = True
            for item in positions: # add all the previous lsf ID's
                storeLsfFormsID.append(item.laborStatusFormID) # store all of the previous labor status forms for break
            laborStatusFormID = storeLsfFormsID.pop() #save all the previous lsf ID's except the one currently created. Pop removes the one created right now.
            formHistoryID = FormHistory.get(FormHistory.formID == laborStatusFormID)
            isMoreLSF_dict['formHistoryID'] = formHistoryID.formHistoryID
            isMoreLSF_dict["lsfFormID"] = storeLsfFormsID
    else:
        isMoreLSF_dict["ShowModal"] = False # Do not show the modal when there's not previous lsf
        isMoreLSF_dict["isMoreLSf"] = False # student does not have any previous lsf's.
    return json.dumps(isMoreLSF_dict)

def checkForPrimaryPosition(termCode, student):
    """ Checks if a student has a primary supervisor (which means they have primary position) in the selected term. """
    rsp = (request.data).decode("utf-8")  # This turns byte data into a string
    rspFunctional = json.loads(rsp)
    term = Term.get(Term.termCode == termCode)
    try:
        lastPrimaryPosition = FormHistory.select().join_from(FormHistory, LaborStatusForm).where(FormHistory.formID.termCode == termCode, FormHistory.formID.studentSupervisee == student, FormHistory.historyType == "Labor Status Form", FormHistory.formID.jobType == "Primary").order_by(FormHistory.formHistoryID.desc()).get()
    except DoesNotExist:
        lastPrimaryPosition = None

    if not lastPrimaryPosition:
        approvedRelease = None
    else:
        try:
            approvedRelease = FormHistory.select().where(FormHistory.formID == lastPrimaryPosition.formID, FormHistory.historyType == "Labor Release Form", FormHistory.status == "Approved").order_by(FormHistory.formHistoryID.desc()).get()
        except DoesNotExist:
            approvedRelease = None

    finalStatus = ""
    if not term.isBreak:
        if lastPrimaryPosition and not approvedRelease:
            if rspFunctional == "Primary":
                if lastPrimaryPosition.status.statusName == "Denied":
                    finalStatus = "hire"
                else:
                    finalStatus = "noHire"
            else:
                if lastPrimaryPosition.status.statusName == "Approved" or lastPrimaryPosition.status.statusName == "Approved Reluctantly":
                    finalStatus = "hire"
                else:
                    finalStatus = "noHireForSecondary"
        elif lastPrimaryPosition and approvedRelease:
            if rspFunctional == "Primary":
                finalStatus = "hire"
            else:
                finalStatus = "noHireForSecondary"
        else:
            if rspFunctional == "Primary":
                finalStatus = "hire"
            else:
                finalStatus = "noHireForSecondary"
    else:
        finalStatus = "hire"
    return json.dumps(finalStatus)

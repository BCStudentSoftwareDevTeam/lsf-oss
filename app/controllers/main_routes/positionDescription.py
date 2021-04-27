from flask_login import login_required
from app.controllers.main_routes import *
from app.login_manager import require_login
from app.models.user import *
from app.models.formHistory import *
from app.models.positionDescription import *
from app.models.positionDescriptionItem import *
from app.models.position import *
from flask import json, jsonify
from flask import request
from datetime import datetime, date, timedelta
from flask import Flask, redirect, url_for, flash
from app import cfg
from app.logic.emailHandler import*
from app.logic.userInsertFunctions import*

@main_bp.route('/positionDescriptions', methods=['GET'])
def PositionDescriptionView():
    """ Render Position Description Form"""
    currentUser = require_login()
    if not currentUser:        # Not logged in
        return render_template('errors/403.html'), 403
    if not currentUser.isLaborAdmin:
        if currentUser.student and not currentUser.supervisor:
            return redirect('/laborHistory/' + currentUser.student.ID)
        if not currentUser.student and currentUser.supervisor:
            # Checks all the forms where the current user has been the creator or the supervisor, and grabs all the departments associated with those forms. Will only grab each department once.
            departments = FormHistory.select(FormHistory.formID.department.DEPT_NAME, FormHistory.formID.department.ACCOUNT, FormHistory.formID.department.ORG) \
                            .join_from(FormHistory, LaborStatusForm) \
                            .join_from(LaborStatusForm, Department) \
                            .where((FormHistory.formID.supervisor == currentUser.supervisor.ID) | (FormHistory.createdBy == currentUser)) \
                            .order_by(FormHistory.formID.department.DEPT_NAME.asc()) \
                            .distinct()

    if currentUser.isLaborAdmin:
        # Grabs every single department that currently has at least one labor status form in it
        departments = FormHistory.select(FormHistory.formID.department.DEPT_NAME, FormHistory.formID.department.ACCOUNT, FormHistory.formID.department.ORG) \
                        .join_from(FormHistory, LaborStatusForm) \
                        .join_from(LaborStatusForm, Department) \
                        .order_by(FormHistory.formID.department.DEPT_NAME.asc()) \
                        .distinct()

    # Logged in
    todayDate = date.today()
    openTerms = Term.select().where(Term.termEnd > todayDate)
    closedTerms = Term.select().where(Term.termEnd < todayDate)

    return render_template( 'main/positionDescription.html',
				            title=('Position Description'),
                            UserID = currentUser,
                            openTerms = openTerms,
                            closedTerms = closedTerms,
                            departments = departments)

@main_bp.route("/positionDescriptions/getPositions/<departmentOrg>/<departmentAcct>", methods=['GET'])
def getDepartmentPositions(departmentOrg, departmentAcct):
    """ Get all of the positions that are in the selected department """
    positions = Tracy().getPositionsFromDepartment(departmentOrg,departmentAcct)
    positionDict = {}
    for position in positions:
        positionDict[position.POSN_CODE] = {"position": position.POSN_TITLE, "WLS":position.WLS, "positionCode":position.POSN_CODE}
    return json.dumps(positionDict)

@main_bp.route("/positionDescriptions/getVersions", methods=['POST'])
def getVersions():
    """ Get all of the positions that are in the selected department """
    try:
        rsp = eval(request.data.decode("utf-8"))
        returnDict = {}
        versions = PositionDescription.select().where(PositionDescription.POSN_CODE == rsp["POSN_CODE"])
        for version in versions:
            if not version.endDate:
                returnDict[version.positionDescriptionID] = {"createdDate": version.createdDate.strftime('%m/%d/%y'), "endDate": "None", "status": version.status.statusName}
            else:
                returnDict[version.positionDescriptionID] = {"createdDate": version.createdDate.strftime('%m/%d/%y'), "endDate": version.endDate.strftime('%m/%d/%y'), "status": version.status.statusName}
        return jsonify(returnDict)
    except Exception as e:
        print ("ERROR", e)

@main_bp.route("/positionDescriptions/checkDescription", methods=['POST'])
def checkDescription():
    """ Check to see if there is already a description for a position in the database """
    try:
        rsp = eval(request.data.decode("utf-8"))
        ## TODO will there be an entry for the position in positionDescription table if there are no description?? 
        selectedPosition = PositionDescription.select().where(PositionDescription.POSN_CODE == rsp["POSN_CODE"])

    except Exception as e:
        print ("ERROR", e)

@main_bp.route("/positionDescriptions/getPositionDescription", methods=['POST'])
def getDescription():
    """ Get all of the positions that are in the selected department """
    try:
        rsp = eval(request.data.decode("utf-8"))
        returnList = []
        positionDescriptionQualifications = PositionDescriptionItem.select().where((PositionDescriptionItem.itemType == "Qualification") & (PositionDescriptionItem.positionDescription == rsp["positionDescriptionID"]))
        positionDescriptionLearningOBJ = PositionDescriptionItem.select().where((PositionDescriptionItem.positionDescription == rsp["positionDescriptionID"]) & (PositionDescriptionItem.itemType == "Learning Objective"))
        positionDescriptionDuty = PositionDescriptionItem.select().where((PositionDescriptionItem.positionDescription == rsp["positionDescriptionID"]) & (PositionDescriptionItem.itemType == "Duty"))
        returnList.append("<p><strong>Qualifications</strong></p>")
        for item in positionDescriptionQualifications:
            returnList.append("<p>" + item.itemDescription + "</p>")
        returnList.append("<p><strong>Learning Objectives</strong></p>")
        for item in positionDescriptionLearningOBJ:
            returnList.append("<p>" + item.itemDescription + "</p>")
        returnList.append("<p><strong>Duties</strong></p>")
        for item in positionDescriptionDuty:
            returnList.append("<p>" + item.itemDescription + "</p>")
        return jsonify(returnList)
    except Exception as e:
        print ("ERROR", e)

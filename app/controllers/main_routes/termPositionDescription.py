from flask_login import login_required
from app.controllers.main_routes import *
from app.login_manager import require_login
from app.models.user import *
from app.models.formHistory import *
from flask import json, jsonify
from flask import request
from datetime import datetime, date, timedelta
from flask import Flask, redirect, url_for, flash
from app import cfg
from app.logic.emailHandler import*
from app.logic.userInsertFunctions import*

@main_bp.route('/termPositionDescription', methods=['GET'])
def termPositionDescription():
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
    print(todayDate)
    openTerms = Term.select().where(Term.termEnd > todayDate)
    closedTerms = Term.select().where(Term.termEnd < todayDate)

    return render_template( 'main/termPositionDescription.html',
				            title=('Position Description'),
                            UserID = currentUser,
                            openTerms = openTerms,
                            closedTerms = closedTerms,
                            departments = departments)

@main_bp.route("/termPositionDescription/getPositions/<departmentOrg>/<departmentAcct>", methods=['GET'])
def getDepartmentPositions(departmentOrg, departmentAcct):
    """ Get all of the positions that are in the selected department """
    positions = Tracy().getPositionsFromDepartment(departmentOrg,departmentAcct)
    positionDict = {}
    for position in positions:
        positionDict[position.POSN_CODE] = {"position": position.POSN_TITLE, "WLS":position.WLS, "positionCode":position.POSN_CODE}
    return json.dumps(positionDict)

@main_bp.route("/termPositionDescription/getPositionDescription", methods=['POST'])
def getPositionDescription():
    """ Get all of the positions that are in the selected department """
    print("Hello inside the the controller")
    rsp = eval(request.data.decode("utf-8"))
    print(rsp)
    positionDescription, created = TermPositionDescription.get_or_create(termCode = rsp["termCode"],
                                                                        POSN_CODE = rsp["positionCode"])
    if positionDescription:
        return positionDescription
    return created

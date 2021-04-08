from flask_login import login_required
from app.controllers.main_routes import *
from app.login_manager import require_login
from app.models.user import *
from app.models.formHistory import *
from app.models.position import *
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

@main_bp.route('/positionDescriptionEdit/<positionDescriptionID>', methods=['GET'])
def PositionDescriptionEdit(positionDescriptionID):
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

    positionDescriptionItems = PositionDescriptionItem.select().where(PositionDescriptionItem.positionDescription == positionDescriptionID)

    return render_template( 'main/positionDescriptionEdit.html',
				            title=('Position Description'),
                            UserID = currentUser,
                            departments = departments,
                            positionDescriptionItems = positionDescriptionItems)

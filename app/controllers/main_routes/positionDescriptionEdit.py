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
    positionDescriptionRecord = PositionDescription.select().where(PositionDescription.positionDescriptionID == positionDescriptionID).get()

    distinctTypes = PositionDescriptionItem.select(PositionDescriptionItem.itemType).distinct()
    itemTypes=[]
    for type in distinctTypes:
        itemTypes.append(type.itemType)

    return render_template( 'main/positionDescriptionEdit.html',
				            title=('Position Description'),
                            UserID = currentUser,
                            departments = departments,
                            positionDescriptionItems = positionDescriptionItems,
                            itemTypes = itemTypes,
                            positionDescriptionRecord = positionDescriptionRecord)

@main_bp.route("/positionDescriptionEdit/submitRevisions", methods=['POST'])
def submitRevisions():
    """ Get all of the positions that are in the selected department """
    try:
        currentUser = require_login()
        rsp = eval(request.data.decode("utf-8"))
        position = Position.select().where(Position.POSN_CODE == rsp["positionCode"]).get()
        positionDescription = PositionDescription.create( createdBy = currentUser,
                                                          status = "Pending",
                                                          POSN_CODE = rsp["positionCode"],
                                                          createdDate = date.today()
                                                        )
        for duty in rsp["duties"]:
            PositionDescriptionItem.create( positionDescription = positionDescription ,
                                            itemDescription = duty,
                                            itemType = "Duty"
                                          )
        for qualification in rsp["qualifications"]:
            PositionDescriptionItem.create( positionDescription = positionDescription ,
                                            itemDescription = qualification,
                                            itemType = "Qualification"
                                          )
        for learningObjective in rsp["learningObjectives"]:
            PositionDescriptionItem.create( positionDescription = positionDescription ,
                                            itemDescription = learningObjective,
                                            itemType = "Learning Objective"
                                          )
        message = "Your position description revision for {0} ({1}) - {2} has been submited.".format(position.POSN_TITLE, position.WLS, position.POSN_CODE)
        flash(message, "success")
        return jsonify({"Success":True})
    except Exception as e:
        print ("ERROR", e)
        return jsonify({"Success": False})

@main_bp.route("/positionDescriptionEdit/adminUpdate", methods=['POST'])
def adminUpdate():
    """ Get all of the positions that are in the selected department """
    try:
        currentUser = require_login()
        rsp = eval(request.data.decode("utf-8"))
        position = PositionDescription.select().where(PositionDescription.POSN_CODE == rsp["positionCode"]).get()
        if rsp["adminChoice"] == "Deny":
            position.status = "Denied"
            position.save()
            message = "The position description revision for {0} ({1}) - {2} has been denied.".format(position.POSN_CODE.POSN_TITLE, position.POSN_CODE.WLS, position.POSN_CODE.POSN_CODE)
            messageType = "danger"
        elif rsp["adminChoice"] == "Approve":
            print("Inside Approve")
            descriptionItems = PositionDescriptionItem.select().where(PositionDescriptionItem.positionDescription == position.positionDescriptionID)
            for item in descriptionItems:
                print(item)
            message = "The position description revision for {0} ({1}) - {2} has been approved.".format(position.POSN_CODE.POSN_TITLE, position.POSN_CODE.WLS, position.POSN_CODE.POSN_CODE)
            messageType = "success"
        # flash(message, messageType)
        return jsonify({"Success":True})
    except Exception as e:
        print ("ERROR", e)
        return jsonify({"Success": False})

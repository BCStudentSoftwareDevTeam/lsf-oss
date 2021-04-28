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
@main_bp.route('/positionDescriptionEdit/newVersion/<positionCode>', methods=['GET'])
def PositionDescriptionEdit(positionDescriptionID = None, positionCode = None):
    """ Render Position Description Form"""
    currentUser = require_login()
    if not currentUser:        # Not logged in
        return render_template('errors/403.html'), 403
    if not currentUser.isLaborAdmin:
        if currentUser.student and not currentUser.supervisor:
            return redirect('/laborHistory/' + currentUser.student.ID)

    print(positionDescriptionID, positionCode)
    if positionDescriptionID:
        positionDescriptionItems = PositionDescriptionItem.select().where(PositionDescriptionItem.positionDescription == positionDescriptionID)
        positionDescriptionRecord = PositionDescription.select().where(PositionDescription.positionDescriptionID == positionDescriptionID).get()
        positionRecord = Position.select().where(Position.POSN_CODE == positionDescriptionRecord.POSN_CODE.POSN_CODE).get()
    elif positionCode:
        positionDescriptionItems = None
        positionDescriptionRecord = None
        positionRecord = Position.select().where(Position.POSN_CODE == positionCode).get()

    pendingPositionDescription = PositionDescription.select().where(PositionDescription.POSN_CODE == positionRecord.POSN_CODE)

    if not currentUser.isLaborAdmin:
        # Checks all the forms where the current user has been the creator or the supervisor, and grabs all the departments associated with those forms. Will only grab each department once.
        if pendingPositionDescription:
            for record in pendingPositionDescription:
                if record.status.statusName == "Pending":
                    return render_template('errors/403.html'), 403

        authorizedUser = False
        departments = FormHistory.select(FormHistory.formID.department.DEPT_NAME, FormHistory.formID.department.ACCOUNT, FormHistory.formID.department.ORG) \
                        .join_from(FormHistory, LaborStatusForm) \
                        .join_from(LaborStatusForm, Department) \
                        .where((FormHistory.formID.supervisor == currentUser.supervisor.ID) | (FormHistory.createdBy == currentUser)) \
                        .order_by(FormHistory.formID.department.DEPT_NAME.asc()) \
                        .distinct()
        for department in departments:
            if department.formID.department.DEPT_NAME == positionRecord.DEPT_NAME:
                authorizedUser = True
                break
        if not authorizedUser:
            return render_template('errors/403.html'), 403

    itemTypes = ['Learning Objective', 'Qualification', 'Duty']

    return render_template( 'main/positionDescriptionEdit.html',
                            showModal=True,
				            title=('Position Description'),
                            UserID = currentUser,
                            positionDescriptionItems = positionDescriptionItems,
                            itemTypes = itemTypes,
                            positionDescriptionRecord = positionDescriptionRecord,
                            positionRecord = positionRecord)

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
        position = PositionDescription.select().where(PositionDescription.positionDescriptionID == rsp["recordID"]).get()
        if rsp["adminChoice"] == "Deny":
            position.status = "Denied"
            position.save()
            message = "The position description revision for {0} ({1}) - {2} has been denied.".format(position.POSN_CODE.POSN_TITLE, position.POSN_CODE.WLS, position.POSN_CODE.POSN_CODE)
            messageType = "danger"
        elif rsp["adminChoice"] == "Approve":
            descriptionItems = PositionDescriptionItem.select().where(PositionDescriptionItem.positionDescription == position.positionDescriptionID)
            try:
                lastPositionDescription = PositionDescription.select().where((PositionDescription.POSN_CODE == position.POSN_CODE) & (PositionDescription.status == "Approved")).order_by(PositionDescription.createdDate.desc())[0]
            except:
                lastPositionDescription = None
            if lastPositionDescription:
                lastPositionDescription.endDate = date.today()
                lastPositionDescription.save()
            position.status = "Approved"
            position.save()
            for item in descriptionItems:
                item.delete_instance()
            for duty in rsp["duties"]:
                PositionDescriptionItem.create( positionDescription = position.positionDescriptionID,
                                                itemDescription = duty,
                                                itemType = "Duty"
                                              )
            for qualification in rsp["qualifications"]:
                PositionDescriptionItem.create( positionDescription = position.positionDescriptionID,
                                                itemDescription = qualification,
                                                itemType = "Qualification"
                                              )
            for learningObjective in rsp["learningObjectives"]:
                PositionDescriptionItem.create( positionDescription = position.positionDescriptionID,
                                                itemDescription = learningObjective,
                                                itemType = "Learning Objective"
                                              )
            message = "The position description revision for {0} ({1}) - {2} has been approved.".format(position.POSN_CODE.POSN_TITLE, position.POSN_CODE.WLS, position.POSN_CODE.POSN_CODE)
            messageType = "success"
        flash(message, messageType)
        return jsonify({"Success":True})
    except Exception as e:
        print ("ERROR On Admin Position Description Update:", e)
        return jsonify({"Success": False})

from app.controllers.admin_routes import *
from app.models.user import User
from app.controllers.admin_routes import admin
from app.login_manager import require_login
from app.models.term import Term
from app.models.positionDescription import *
from app.models.positionDescriptionItem import *
from app.models.position import *
from datetime import datetime
from flask import json, jsonify
from flask import request, redirect
from peewee import IntegrityError

@admin.route('/admin/viewPositionDescriptions', methods=['GET', 'POST'])
# @login_required

def viewPositionDescriptions():
    currentUser = require_login()
    if not currentUser:                    # Not logged in
        return render_template('errors/403.html')
    if not currentUser.isLaborAdmin:       # Not an admin
        if currentUser.student: # logged in as a student
            return redirect('/laborHistory/' + currentUser.student.ID)
        elif currentUser.supervisor:
            return render_template('errors/403.html'), 403

    pendingPositionDescriptions = PositionDescription.select().where(PositionDescription.status == "Pending")

    for i in pendingPositionDescriptions:
        print(i)


    return render_template( 'admin/viewPositionDescriptions.html',
                             title='Term Management',
                             pendingPositionDescriptions = pendingPositionDescriptions
                          )

from app.controllers.main_routes import *
from app.models.user import *
from app.models.laborReleaseForm import *
from app.models.formHistory import *
from app.models.laborStatusForm import *
from flask_bootstrap import bootstrap_find_resource
from app.models.student import *
from app.models.department import *
from app.models.user import *
from app.controllers.errors_routes.handlers import *
from app.login_manager import require_login
from flask import Flask, redirect, url_for
from flask import request
from flask import jsonify

@main_bp.route('/laborReleaseForm', methods=['GET', 'POST'])
# @login_required
def laborReleaseForm():

    current_user = require_login()
    if not current_user:
        render_template("errors/403.html")
    if not current_user.isLaborAdmin:
        render_template("errors/403.html")

    students = Student.select()
    department = Department.select()
    users = User.select()
    forms = LaborStatusForm.select().distinct().where(LaborStatusForm.laborStatusFormID == 21) #FIXEME: This ID needs to come from the modal from the supervisor portal
    #forms = FormHistory.select().distinct().where(FormHistory.formHistoryID == 1)

    return render_template( 'main/laborReleaseForm.html',
				            title=('Labor Release Form'),
                            students = students,
                            department = department,
                            users = users,
                            forms = forms
                          )

@main_bp.route("/index/second", methods=['POST'])

def createReleaseForm():
    try:
        print("Made it into the try")
        date = request.form.get("date")
        print (date)
        reason = request.form.get("notes")
        print (reason)
        condition = request.form.get("condition")
        print (condition)
        #rsp = eval(request.data.decode("utf-8"))
        return redirect(url_for("main.index"))

    except Exception as e:
        print(e)
        return jsonify({"Success": False})

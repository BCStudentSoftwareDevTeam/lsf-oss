from app.controllers.main_routes import *
from app.models.user import *
from app.models.laborStatusForm import *
from app.models.term import *
from flask_bootstrap import bootstrap_find_resource
from app.models.Tracy.studata import *
from app import *
from app.login_manager import *


@app.route("/contributors", methods = ["GET"])
def contributors():
    current_user = require_login()
    if not current_user:        # Not logged in
        return render_template('errors/403.html')
    if not current_user.isLaborAdmin:       # Not an admin
        isLaborAdmin = False
        if current_user.Student:
            isStudent = True
        else:
            isStudent = False
    else:
        if current_user.Student:
            isStudent = True
        else:
            isStudent = False

    contribs = load_config("app/config/contributors.yaml")
    return render_template("main/contributors.html",
           cfg=contribs,
           isLaborAdmin = isLaborAdmin,
           isStudent = isStudent,
           current_user = current_user
           )

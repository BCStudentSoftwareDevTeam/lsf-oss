from app.controllers.main_routes import *
from app.models.user import *
from app.models.laborStatusForm import *
from app.models.term import *
from flask_bootstrap import bootstrap_find_resource
from app.models.Tracy.studata import *
from app import *


@app.route("/contributors", methods = ["GET"])
def contributors():
    contribs = load_config("app/config/contributors.yaml")
    return render_template("main/contributors.html",
           cfg=contribs

           )

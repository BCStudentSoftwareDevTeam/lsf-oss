from app.controllers.admin_routes import *
from app.models.user import *
from app.controllers.admin_routes import admin
from app.models.term import *


@admin.route('/termManagement', methods=['GET', 'POST'])
# @login_required
def term_Management():
    term = Term.select()
    termStart = Term.select()
    termEnd = Term.select()
    termState = Term.select()
    return render_template( 'admin/termManagement.html',
				            title=('Admin Management'),
                            term = term,
                            termStart = termStart,
                            termEnd = termEnd,
                            termState = termState
                          )

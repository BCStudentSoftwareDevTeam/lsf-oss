from app.controllers.admin_routes import *
from app.models.user import *
from app.controllers.admin_routes import admin
from app.models.term import *
import datetime


@admin.route('/termManagement', methods=['GET', 'POST'])
# @login_required
def term_Management():
    terms = Term.select()
    termStart = Term.select()
    termEnd = Term.select()
    termState = Term.select()
    termCode = Term.select()
    termName = Term.select()
    orderedTerms = Term.select().order_by(Term.termCode).order_by(Term.termStart)
    # x = 0
    # for Term.termCode in Term.select():
    #     print(x)
    #     print(orderedTerms[x].termCode, orderedTerms[x].termName, orderedTerms[x].termStart, orderedTerms[x].termEnd)
    #     x = x + 1
    return render_template( 'admin/termManagement.html',
				             title=('Admin Management'),
                             terms = orderedTerms,
                             termStart = termStart,
                             termEnd = termEnd,
                             termState = termState,
                             termCode = termCode,
                             termName = termName
                          )

def createTerm():
    today = datetime.datetime.now()
    print(today)
    print(today.year)
    print(today.year - 2)
    print(today.year + 2)

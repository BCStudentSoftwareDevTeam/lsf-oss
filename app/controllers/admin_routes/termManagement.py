from app.controllers.admin_routes import *
from app.models.user import User
from app.controllers.admin_routes import admin
from app.login_manager import require_login
from app.models.term import Term
import datetime
from flask import json, jsonify
from flask import request, redirect
from datetime import datetime, date
from datetime import datetime
import datetime

@admin.route('/admin/termManagement', methods=['GET', 'POST'])
# @login_required

def term_Management():
    currentUser = require_login()
    if not currentUser:                    # Not logged in
        return render_template('errors/403.html')
    if not currentUser.isLaborAdmin:       # Not an admin
        if currentUser.Student: # logged in as a student
            return redirect('/laborHistory/' + currentUser.Student.ID)
        elif currentUser.Supervisor:
            return render_template('errors/403.html',
                                currentUser = currentUser)

    terms = Term.select()
    listOfTerms = Term.select()
    for i in range(5):
        createTerms(Term, i)
    accordionTerms()
    return render_template( 'admin/termManagement.html',
                             title=('Term Management'),
                             terms = terms,
                             listOfTerms = accordionTerms(),
                             currentUser = currentUser
                          )

def createTerms(termList, iteration):
    """ This function creates the current Academic Year, two Academic years in the past and two Academic
    Years in the future. If any of the terms that are in the Academic Years are already created it will
    get an exception message. """
    today = datetime.datetime.now()
    todayYear = today.year
    termYear = todayYear - 2 + iteration
    code = (todayYear - 2 + iteration) * 100
    for i in range(7):
        try:
            if i == 0:
                termList.create(termCode = code, termName = ("AY " + str(termYear) + "-" + str(termYear + 1)))
            elif i == 1:
                termList.create(termCode = (code + 11), termName = ("Fall " + str(termYear)))
            elif i == 2:
                termList.create(termCode = (code + 1), termName = ("Thanksgiving Break " + str(termYear)), isBreak = True)
            elif i == 3:
                termList.create(termCode = (code + 2), termName = ("Christmas Break " + str(termYear)), isBreak = True)
            elif i == 4:
                termList.create(termCode = (code + 12), termName = ("Spring " + str(termYear + 1)))
            elif i == 5:
                termList.create(termCode = (code + 3), termName = ("Spring Break " + str(termYear + 1)), isBreak = True)
            elif i == 6:
                termList.create(termCode = (code + 13), termName = ("Summer " + str(termYear + 1)), isBreak = True, isSummer = True)
        except Exception as e:
             print("You failed to create a term in the " + str(termYear) + " AY. This is likely expected.")

def accordionTerms():
    """ This function populates all the Academic Years with the correct terms.
    """
    listOfTerms = []
    hoy = datetime.datetime.now()
    hoyyear = hoy.year
    for i in range(5):
        termYear = (hoyyear - 2 + i)*100
        currentTerm = Term.select().where(Term.termCode.between(termYear-1, termYear + 15))
        listOfTerms.append([])
        for term in currentTerm:
            listOfTerms[i].append(term)
    return listOfTerms

@admin.route("/termManagement/setDate/", methods=['POST'])
def ourDate():
    """ This function updates the dates so that they are correctly formatted to be inserted into the
    database.
    """
    try:
        rsp = eval(request.data.decode("utf-8"))
        if rsp:
            termCode = rsp['termCode']
            termToChange = Term.get(Term.termCode == termCode)
            date_value = rsp.get("start", rsp.get("end", rsp.get("primaryCutOff", rsp.get("adjustmentCutOff", None))))
            if rsp.get('start', None):
                startDate = datetime.datetime.strptime(date_value, '%m/%d/%Y').strftime('%Y-%m-%d')
                termToChange.termStart = startDate
                dateChanged = 'Start Date'
            if rsp.get('end', None):
                endDate = datetime.datetime.strptime(date_value, '%m/%d/%Y').strftime('%Y-%m-%d')
                termToChange.termEnd = endDate
                dateChanged = 'End Date'
            if rsp.get('primaryCutOff', None):
                primaryCutOff = datetime.datetime.strptime(date_value, '%m/%d/%Y').strftime('%Y-%m-%d')
                termToChange.primaryCutOff = primaryCutOff
                dateChanged = 'Primary Cut Off Date'
            if rsp.get('adjustmentCutOff', None):
                adjustmentCutOff = datetime.datetime.strptime(date_value, '%m/%d/%Y').strftime('%Y-%m-%d')
                termToChange.adjustmentCutOff = adjustmentCutOff
                dateChanged = 'Adjustment Cut Off Date'
            termToChange.save()
            flasherInfo = {'changedTerm': termToChange.termName,
                            'newDate': date_value,
                            'dateChanged': dateChanged
            }
            return jsonify(flasherInfo)
    except Exception as e:
        print("You have failed to update the date.", e)
        return jsonify({"Success": False})


@admin.route('/termManagement/manageStatus', methods=['POST'])
def termStatusCheck():
    """ This function updates the state of the term
    """
    try:
        rsp = eval(request.data.decode("utf-8")) # This fixes byte indices must be intergers or slices error
        if rsp:
            term = Term.get(rsp['termBtn'])

            if term.termState == True:
                term.termState = False
            elif term.termState == False:
                term.termState = True
            term.save()
            flasherInfo = {'termChanged': term.termName}
            return jsonify(flasherInfo)
    except Exception as e:
        print(e)
        return jsonify({"Success": False})

from app.controllers.admin_routes import *
from app.models.user import *
from app.controllers.admin_routes import admin
from app.models.term import *
import datetime
from app.models.term import *
from flask import json, jsonify
from flask import request
from datetime import datetime, date
from datetime import datetime
import datetime

@admin.route('/admin/termManagement', methods=['GET', 'POST'])
# @login_required
def term_Management():
    terms = Term.select()
    listOfTerms = Term.select()
    for i in range(5):
        createTerms(Term, i)
    accordionTerms()
    return render_template( 'admin/termManagement.html',
                             title=('Admin Management'),
                             terms = terms,
                             listOfTerms = accordionTerms()
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
                termList.create(termCode = (code + 1), termName = ("Thanksgiving Break " + str(termYear)))
            elif i == 3:
                termList.create(termCode = (code + 2), termName = ("Christmas Break " + str(termYear)))
            elif i == 4:
                termList.create(termCode = (code + 12), termName = ("Spring " + str(termYear + 1)))
            elif i == 5:
                termList.create(termCode = (code + 3), termName = ("Spring Break " + str(termYear + 1)))
            elif i == 6:
                termList.create(termCode = (code + 13), termName = ("Summer " + str(termYear + 1)))
        except Exception as e:
            # print("You failed to create a term in the " + str(termYear) + " AY.")

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
    # print(listOfTerms)
    return listOfTerms

@admin.route("/termManagement/setDate/", methods=['POST'])
def ourDate():
    """ This function updates the dates so that they are correctly formatted to be inserted into the
    database.
    """
    try:
        rsp = eval(request.data.decode("utf-8"))
        # print(rsp)
        if rsp:
            print("success")
            termCode = rsp['termCode']
            termToChange = Term.get(Term.termCode == termCode)
            date_value = rsp.get("start", rsp.get("end", None))
            # print(date_value)
            if rsp.get('start', None):
                startDate = datetime.datetime.strptime(date_value, '%m/%d/%Y').strftime('%Y-%m-%d')
                termToChange.termStart = startDate
                # print("startDate saved")
            if rsp.get('end', None):
                endDate = datetime.datetime.strptime(date_value, '%m/%d/%Y').strftime('%Y-%m-%d')
                termToChange.termEnd = endDate
                # print("endDate saved")
            termToChange.save()
            return jsonify({"Success": True})
    except Exception as e:
        # print("You have failed to update the date.", e)
        return jsonify({"Success": False})


@admin.route('/termManagement/manageStatus', methods=['POST'])
def termStatusCheck():
    """ This function updates the state of the term
    """
    try:
    #print("Get request")
        rsp = eval(request.data.decode("utf-8")) # This fixes byte indices must be intergers or slices error
        print(rsp)
        if rsp:
            term = Term.get(rsp['termBtn'])
            # print("this is the term " + str(term))
            # print(term.termState)
            if term.termState == True:
                term.termState = False
            elif term.termState == False:
                term.termState = True
            # print(term.termState)
            term.save()
            # print("worked")
            return jsonify({"Success": True})
    except Exception as e:
        # print(e)
        return jsonify({"Success": False})

from app.controllers.admin_routes import *
from app.models.user import *
from app.controllers.admin_routes import admin
from app.models.term import *
import datetime
from app.models.term import *
from flask import json, jsonify
from flask import request
from datetime import datetime, date
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
    listOfTerms = Term.select()
    for i in range(5):
        createTerms(Term, i)
    accordionTerms()
    # orderedTerms = Term.select().order_by(Term.termCode).order_by(Term.termStart)
    # singleTerm = Term.select().where(Term.termCode >= 201900)
    return render_template( 'admin/termManagement.html',
                             title=('Admin Management'),
                             terms = terms,
                             # orderedTerms = orderedTerms,
                             termStart = termStart,
                             termEnd = termEnd,
                             termState = termState,
                             termCode = termCode,
                             termName = termName,
                             listOfTerms = accordionTerms()
                          )
def createTerms(termList, iteration):
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
                termList.create(termCode = (code + 1), termName = ("ThanksGiving Break " + str(termYear)))
            elif i == 3:
                termList.create(termCode = (code + 2), termName = ("Christmas Break " + str(termYear)))
            elif i == 4:
                termList.create(termCode = (code + 12), termName = ("Spring " + str(termYear + 1)))
            elif i == 5:
                termList.create(termCode = (code + 3), termName = ("Spring Break " + str(termYear + 1)))
            elif i == 6:
                termList.create(termCode = (code + 13), termName = ("Summer " + str(termYear + 1)))
        except Exception as e:
            print("You failed to create a term in the " + str(termYear) + " AY.")

def accordionTerms():
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

@admin.route("/termManagement/getStartDate/", methods=['POST'])
def ourDate():
    try:
        print("Hi")
        rsp = eval(request.data.decode("utf-8"))
        print(rsp)
        print("Hi World")
        if rsp:
            print("success")
            for data in rsp.values():
                code_index = data['termCode']
                date_index = data['start date']
                startDate = datetime.datetime.strptime(date_index, '%m/%d/%Y').strftime('%Y-%m-%d')
                print("startDate")
                termToChange = Term.get(Term.termCode == code_index)
                (termToChange).termStart = startDate
                termToChange.save()
                print("You got it!")
                return jsonify({"Success": True})
    except Exception as e:
        print("You have failed to update the date.")
        return jsonify({"Success": False})

@admin.route("/termManagement/getEndDate/", methods=['POST'])
def nuestroDate():
    try:
        print("Hi")
        rsp = eval(request.data.decode("utf-8"))
        print(rsp)
        print("Hi World")
        if rsp:
            print("success")
            for data in rsp.values():
                code_index = data['termCode']
                date_index = data['end date']
                endDate = datetime.datetime.strptime(date_index, '%m/%d/%Y').strftime('%Y-%m-%d')
                print("startDate")
                termToChange = Term.get(Term.termCode == code_index)
                (termToChange).termEnd = endDate
                termToChange.save()
                print("You got it!")
                return jsonify({"Success": True})
    except Exception as e:
        print("You have failed to update the date.")
        return jsonify({"Success": False})

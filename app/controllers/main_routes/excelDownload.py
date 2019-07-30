# from flask import flash
# from app.models.laborStatusForm import LaborStatusForm
# from app.controllers.main_routes.main_routes import *
# from app.controllers.main_routes.download import ExcelMaker
# from flask import send_file
# from os.path import basename
# import os
#
# @main_bp.route('/', methods=['GET'])
# @main_bp.route('/excel/', methods=['GET'])
# def makeExcel(sid):
#     print('here')
#     value =[]
#     for form in active_supervisees:
#         if request.form.get(form.studentSupervisee.ID):
#             value.append( request.form.get(form.studentSupervisee.ID))
#             print(value)
#
#     ExcelMaker(value)
#     # for student in sid:
#     #     form= LaborStatusForm.select(LaborStatusForm.studentSupervisee == student)
#     # # excel = ExcelMaker(1)
#     # print(student)
#     return()

from app.models.positionDescriptionItem import PositionDescriptionItem
from app.controllers.main_routes import *
from app.models.positionDescription import *
from app.models.positionDescriptionItem import *
from app.models.position import *
from datetime import datetime, date, timedelta
import os
import glob

path = 'positions/test' #TODO

lineStart = {"A.", "B.", "C.", "D.", "E.", "F.", "G.", "H.", "I.", "J.", "K.", "L.", "M."
            "O.", "P.", "Q.", "R.", "S.", "T.", "U.", "V.", "W.", "X.", "Y.", "Z."}

for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
        joined = os.path.join(root, name)
        try:
            fileType = str(joined).split(".", 1)[1]
            try:
                if fileType == "txt":
                    f = open(joined, "r")
                    dutyList = []
                    learningList = []
                    qualificationList = []
                    qualificationSection = False
                    learningSection = False
                    dutySection = False
                    appending = False
                    appendLine = ""
                    for line in f:
                        # Grabbing the position title
                        if "Position Title:" in line:
                            titleSplit = line.split(":", 1)
                            positionTitle = titleSplit[1].strip()

                        # Grabbing the position code
                        if "Position Code" in line:
                            tempLine = line.strip()
                            positionCode = tempLine[-6:]
                            wlsSplit = line.split(":", 2)
                            positionWLS = wlsSplit[1].strip()
                            positionWLS = positionWLS[0]

                        # Grabbing the ORG number
                        if "Org" in line:
                            orgSplit = line.split(":", 2)
                            departmentORG = orgSplit[-1].strip()

                        if "Department Name:" in line:
                            departmentSplit = line.split(":", 1)
                            departmentName = departmentSplit[1].strip()
                            departmentName = departmentName[0:-14].strip()

                        # Grabbing the revision year
                        if "Current Revision Year" in line:
                            yearSplit = line.split(":", 1)
                            year = yearSplit[1].strip()

                        # checking to see what section where in
                        if "description of duties" in line.lower():
                            dutySection = True
                            learningSection, qualificationSection = False, False
                        elif "learning opportunities" in line.lower():
                            learningSection = True
                            qualificationSection, dutySection = False, False
                        elif "qualifications needed" in line.lower():
                            qualificationSection = True
                            learningSection, dutySection = False, False

                        # appending non empty lines into list based on the section
                        if dutySection or qualificationSection or learningSection:
                            line = line.strip()
                            ### If the line does not start with A. or B. ... then we do not need to cut off
                            if "---------" in line:
                                if appendLine:
                                    if appendLine.strip()[0:2] in lineStart:
                                        newLine = appendLine[3:]
                                        newLine = newLine.strip()
                                    else:
                                        newLine = appendLine.strip()
                                    if dutySection:
                                        dutyList.append(newLine)
                                    elif learningSection:
                                        learningList.append(newLine)
                                    elif qualificationSection:
                                        qualificationList.append(newLine)
                                break
                            if line != "":
                                if line[0:2] in lineStart:
                                    if appendLine:
                                        if appendLine.strip()[0:2] in lineStart:
                                            newLine = appendLine[3:]
                                            newLine = newLine.strip()
                                        else:
                                            newLine = appendLine.strip()
                                        if dutySection:
                                            dutyList.append(newLine)
                                        elif learningSection:
                                            learningList.append(newLine)
                                        elif qualificationSection:
                                            qualificationList.append(newLine)
                                    appendLine = ""
                                    appendLine += line
                                elif line[0] not in lineStart:
                                    appendLine +=  " " + line
                            if line == "":
                                if appendLine:
                                    if appendLine.strip()[0:2] in lineStart:
                                        newLine = appendLine[3:]
                                        newLine = newLine.strip()
                                    else:
                                        newLine = appendLine.strip()
                                    if dutySection:
                                        dutyList.append(newLine)
                                    elif learningSection:
                                        learningList.append(newLine)
                                    elif qualificationSection:
                                        qualificationList.append(newLine)
                                    appendLine = ""

                    #need to pop off the first item of each list because it is the
                    # section header
                    dutyList.pop(0)
                    learningList.pop(0)
                    qualificationList.pop(0)

                    try:
                        duplicatePosition = Position.get(Position.POSN_CODE == positionCode)
                        if duplicatePosition:
                            break
                    except:
                        position = Position.create( POSN_CODE = positionCode,
                                                    POSN_TITLE = positionTitle,
                                                    WLS = positionWLS,
                                                    ORG = departmentORG,
                                                    ACCOUNT = departmentORG,
                                                    DEPT_NAME = departmentName)

                        positionDescription = PositionDescription.create( createdBy = 1,
                                                                          status = "Approved",
                                                                          POSN_CODE = position,
                                                                          createdDate = date.today()
                                                                        )

                        for duty in dutyList:
                            PositionDescriptionItem.create( positionDescription = positionDescription.positionDescriptionID,
                                                            itemDescription = duty,
                                                            itemType = "Duty"
                                                          )
                        for qualification in qualificationList:
                            PositionDescriptionItem.create( positionDescription = positionDescription.positionDescriptionID,
                                                            itemDescription = qualification,
                                                            itemType = "Qualification"
                                                          )
                        for learningObjective in learningList:
                            PositionDescriptionItem.create( positionDescription = positionDescription.positionDescriptionID,
                                                            itemDescription = learningObjective,
                                                            itemType = "Learning Objective"
                                                          )
                    print("Succesful Input of:", joined, positionTitle, positionCode)
            except Exception as e:
                print("Error on file: ", joined, ":", positionCode)
                print("ERROR: ", e)
        except Exception as e:
            print("Error on file: ", joined)
            print("ERROR: ", e)

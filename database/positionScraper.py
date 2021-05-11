from app.models.positionDescriptionItem import PositionDescriptionItem
from app.controllers.main_routes import *
from app.models.positionDescription import *
from app.models.positionDescriptionItem import *
from datetime import datetime, date, timedelta
import os
import glob

path = 'positions/chemistry' #TODO

lineStart = {"A.", "B.", "C.", "D.", "E.", "F.", "G.", "H.", "I.", "J.", "K.", "L.", "M."
            "O.", "P.", "Q.", "R.", "S.", "T.", "U.", "V.", "W.", "X.", "Y.", "Z."}

for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
        joined = os.path.join(root, name)
        fileType = str(joined).split(".", 1)[1]
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
                    wls = tempLine[11:12]

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
                    print(line, "the stripped line")
                    if "---------" in line:
                        if appendLine:
                            if dutySection:
                                dutyList.append(appendLine[3:])
                            elif learningSection:
                                learningList.append(appendLine[3:])
                            elif qualificationSection:
                                qualificationList.append(appendLine[3:])
                        break
                    if line != "":
                        if line[0:2] in lineStart:
                            if appendLine:
                                if dutySection:
                                    dutyList.append(appendLine[3:])
                                elif learningSection:
                                    learningList.append(appendLine[3:])
                                elif qualificationSection:
                                    qualificationList.append(appendLine[3:])
                            appendLine = ""
                            appendLine += line
                        elif line[0] not in lineStart:
                            appendLine +=  " " + line
                    if line == "":
                        if appendLine:
                            if dutySection:
                                dutyList.append(appendLine[3:])
                            elif learningSection:
                                learningList.append(appendLine[3:])
                            elif qualificationSection:
                                qualificationList.append(appendLine[3:])
                            appendLine = ""

            #need to pop off the first item of each list because it is the
            # section header
            dutyList.pop(0)
            learningList.pop(0)
            qualificationList.pop(0)
            print(positionTitle,
            "position Title")
            print("This is DUTIES")
            for item in dutyList:
                print(item, "Duty item")
            print("----------------------------------------------------------")
            print("This is LEARNING")
            for item in learningList:
                print(item, "Learning item")
            print("----------------------------------------------------------")
            print("This is QUALIFICATIONS")
            for item in qualificationList:
                print(item, "Qualification item")
            print("----------------------------------------------------------")

            # positionDescription = PositionDescription.create( createdBy = 1,
            #                                                   status = "Approved",
            #                                                   POSN_CODE = positionCode,
            #                                                   createdDate = date.today()
            #                                                 )
            #
            # for duty in dutyList:
            #     PositionDescriptionItem.create( positionDescription = positionDescription.positionDescriptionID,
            #                                     itemDescription = duty,
            #                                     itemType = "Duty"
            #                                   )
            # for qualification in qualificationList:
            #     PositionDescriptionItem.create( positionDescription = positionDescription.positionDescriptionID,
            #                                     itemDescription = qualification,
            #                                     itemType = "Qualification"
            #                                   )
            # for learningObjective in learningList:
            #     PositionDescriptionItem.create( positionDescription = positionDescription.positionDescriptionID,
            #                                     itemDescription = learningObjective,
            #                                     itemType = "Learning Objective"
            #                                   )

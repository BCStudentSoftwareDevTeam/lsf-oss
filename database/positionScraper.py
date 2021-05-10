from app.models.positionDescriptionItem import PositionDescriptionItem
from app.controllers.main_routes import *
from app.models.positionDescription import *
from app.models.positionDescriptionItem import *
from datetime import datetime, date, timedelta
import os
import glob

# directory = 'positions'
# for file in os.walk(directory):
#     # print("Hello?")
#     print(file.path)

# print(glob.glob("/app/database/positions/*.txt"))

for filepath in glob.iglob('positions/*.txt', recursive=True):
    # print(filepath)
    f = open(filepath, "r")
    dutyList = []
    learningList = []
    qualificationList = []
    qualificationSection = False
    learningSection = False
    dutySection = False
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

        # Here, I'm checking to see what section where in
        if "Description Of Duties" in line:
            dutySection = True
            learningSection, qualificationSection = False, False
        elif "Learning Opportunities" in line:
            learningSection = True
            qualificationSection, dutySection = False, False
        elif "Qualifications Needed" in line:
            qualificationSection = True
            learningSection, dutySection = False, False

        # Here, I'm appending non empty lines into list based on the section
        if line.strip() != "":
            if dutySection:
                dutyList.append(line[2:].strip())
            elif learningSection:
                learningList.append(line[2:].strip())
            elif qualificationSection:
                qualificationList.append(line[2:].strip())

    # I need to pop off the first item of each list because it is the
    # section header
    dutyList.pop(0)
    learningList.pop(0)
    qualificationList.pop(0)

    # print("Duties")
    # for i in dutyList:
    #     print(i, "line")
    # print("Learning")
    # for i in learningList:
    #     print(i, "line")
    # print("Qualification")
    # for i in qualificationList:
    #     print(i, "line")

    positionDescription = PositionDescription.create( createdBy = 1,
                                                      status = "Approved",
                                                      POSN_CODE = positionCode,
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

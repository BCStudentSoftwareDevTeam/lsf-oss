import os

positionPath = 'positions/test' #TODD

for root, dirs, files in os.walk(positionPath, topdown=False):

    for name in files:
        joined = os.path.join(root, name)
        replacementName = joined.replace(" ","")

        if(replacementName != joined):
            os.rename(joined,replacementName)

from constants import Actions

keyCode=raw_input("Enter Keyword to Search in Existing Code Directory: ")

if Actions.search(keyCode):
    print "Existing Code Files were found for", keyCode
    Actions.displayExistingCodes(keyCode,loadJson=True)
else:
    print "No Existing Code Files were found for", keyCode
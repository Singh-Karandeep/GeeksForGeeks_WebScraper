from constants import Actions,FilePath
import os

class loadCode:
    def __init__(self):
        self.sortedCodes=None

    def loadExistingCodes(self):
        if os.path.exists(os.path.join(os.getcwd(),FilePath.CODEJSON)):
            count=0
            print "Codes Already Present in Existing Code Directory: "
            self.sortedCodes=sorted(os.listdir(os.path.join(os.getcwd(),FilePath.CODEJSON)))
            for index,code in enumerate(self.sortedCodes):
                print index+1,"\b. ",code

    def execute(self):
        self.loadExistingCodes()
        keyCode = input("Enter Code Number to Search: ")
        if Actions.search(self.sortedCodes[keyCode - 1]):
            print "Existing Code Files were found for", self.sortedCodes[keyCode-1]
            Actions.displayExistingCodes(self.sortedCodes[keyCode-1], loadJson=True)
        else:
            print "No Existing Code Files were found for", self.sortedCodes[keyCode-1]

if __name__=="__main__":
    l = loadCode()
    l.execute()

from constants import Actions,FilePath
import os

class loadCode:
    def __init__(self):
        self.sortedCodes=None

    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False

    def loadExistingCodes(self):
        if os.path.exists(os.path.join(os.getcwd(),FilePath.CODEJSON)):
            print "Codes Already Present in Existing Code Directory: "
            self.sortedCodes=sorted(os.listdir(os.path.join(os.getcwd(),FilePath.CODEJSON)))
            for index,code in enumerate(self.sortedCodes):
                print index+1,"\b. ",code

    def execute(self):
        self.loadExistingCodes()
        keyCode = raw_input("Enter Code Number to Search: ")
        if self.is_number(keyCode):
            keyCode=int(keyCode)
            if keyCode>len(self.sortedCodes) or keyCode<=0:
                print "Enter a valid range"
                exit(1)
        else:
            print "Only digits allowed..."
            exit(2)

        if Actions.search(self.sortedCodes[keyCode - 1]):
            print "Existing Code Files were found for", self.sortedCodes[keyCode-1]
            Actions.displayExistingCodes(self.sortedCodes[keyCode-1], loadJson=True)
        else:
            print "No Existing Code Files were found for", self.sortedCodes[keyCode-1]

if __name__=="__main__":
    l = loadCode()
    l.execute()

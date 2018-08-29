from constants import Actions,FilePath
import os

class loadCode:
    def __init__(self):
        self.sortedCodes=None
        self.linkText=[]
        self.codeDirectory=[]
        self.key=None

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

    def getLinkText(self,keyCode,codeList):
        for index,(key,link) in enumerate(codeList):
            if str(key)==str(keyCode):
                return link
        return False

    def checkExceptions(self,choice):
        if self.is_number(choice):
            keyCode = int(choice)
            if keyCode > len(self.codeDirectory) or keyCode <= 0:
                print "Enter a valid range"
                exit(1)
            return choice
        else:
            print "Only digits allowed..."
            exit(2)

    def execute(self):
        continueFurther=True
        while continueFurther:
            if os.path.exists(FilePath.CODEJSON):
                codeList=[]
                self.codeDirectory=os.listdir(os.path.join(FilePath.CODEJSON))
                if len(self.codeDirectory)>0:
                    print "Existing Code Folders were found for"
                else:
                    print "No Code Directories were found"
                for index,item in enumerate(self.codeDirectory):
                    print index+1,"\b.",item
                    codeList.append([index+1,item])
                choice=raw_input('Enter Folder Option to load Code Files: ')

                self.checkExceptions(choice)

                self.key=self.getLinkText(choice,codeList)
                self.codeDirectory = os.listdir(os.path.join(FilePath.CODEJSON,self.key))
                if len(self.codeDirectory)>0:
                    codeList = []
                    for index,item in enumerate(self.codeDirectory):
                        print index+1,"\b.",item
                        codeList.append([index+1,item])
                    choice = raw_input("Choose Code File to open: ")
                    self.checkExceptions(choice)
                    self.linkText = self.getLinkText(choice, codeList)
                    Actions.displayExistingCodes(self.key,self.linkText,loadJson=True)
                    continueFurther=raw_input('Want to Continue (y/n):')
                else:
                    print "No Code Directories were found inside",self.key
            else:
                print "Codes directory doesn't exists..."

if __name__=="__main__":
    loadCode().execute()
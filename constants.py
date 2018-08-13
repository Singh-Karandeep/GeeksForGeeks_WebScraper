import os,json
from HTMLParser import HTMLParser
from sys import platform

class Globals:
    CC_COMPLIANCE='cc-compliance'
    HREF='href'
    BASE_URL="https://www.geeksforgeeks.org/"
    SEARCH='search'
    SEARCH_BUTTON='gsc-search-button'
    python='python'
    c='c'
    cpp='cpp'
    java='java'

class XPath:
    GS_TITLE='//a[contains(@class,"gs-title")]'

class FilePath:
    CODEJSON='Codes'
    if platform=="win32":
        CHROME_DRIVERPATH = os.path.join(os.getcwd(),'Drivers/chromedriver.exe')
    elif platform == "linux" or platform == "linux2":
        CHROME_DRIVERPATH = os.path.join(os.getcwd(),'Drivers/chromedriver')

class Actions:

    def __init__(self):
        self.Code={}
        self.KEY=None
        self.extension=None
        self.oldStdout=None

    @staticmethod
    def search(key):
        if not os.path.exists(os.path.join(os.getcwd(),FilePath.CODEJSON)):
            print FilePath.CODEJSON,"Directory doesn't exists..."
            return False
        fileList=os.listdir(os.path.join(os.getcwd(),FilePath.CODEJSON))
        if key in fileList:
            return True
        return False

    @staticmethod
    def printCode(code):
        h=HTMLParser()
        for line in code:
            if line is not None:
                print h.unescape(line)

    @staticmethod
    def register(self):
        Actions.Code=self.Code
        Actions.KEY=self.KEY

    @staticmethod
    def finalDump(f,code,extension):
        h = HTMLParser()
        for line in code:
            if line is not None:
                try:
                    f.write(str(h.unescape(line)))
                except Exception as e:
                    f.write("\n@@@@ SOME ERROR ENCOUNTERED AT THIS LINE WHILE DUMPING CODE TO FILE @@@@\n\n")
                    print "\n\n#### Error in saving some code for", extension, " Kindly cross-check once with link."
                    print "#### SOME ERROR HERE HAS BEEN APPENDED IN PLACE OF IT ####"
                    print "--> HOWEVER COMPLETE CODE IS PRESENT IN JSON. YOU CAN FIND BY RUNNING \"loadCode.py\" <--\n"

    @staticmethod
    def dumpToFile(code,extension,index=None):
        if index is None:
            with open(os.path.join(os.getcwd(),FilePath.CODEJSON,Actions.KEY,Actions.KEY+extension),'w')as f:
                Actions.finalDump(f,code,extension)
        else:
            with open(os.path.join(os.getcwd(),FilePath.CODEJSON,Actions.KEY,Actions.KEY+'_'+str(index)+extension),'w')as f:
                Actions.finalDump(f,code,extension)

    @staticmethod
    def exportToFiles():
        with open(os.path.join(os.getcwd(),FilePath.CODEJSON,Actions.KEY,Actions.KEY+'.json'))as f:
            data=json.load(f)

        for index,(language,code) in enumerate(data.items()):
            if language == Globals.python:
                Actions.extension ='.py'
            elif language == Globals.java:
                Actions.extension ='.java'
            elif language == Globals.c:
                Actions.extension ='.c'
            else:
                Actions.extension = '.cpp'

            if len(code)>1:
                for index2,item in enumerate(code):
                    Actions.dumpToFile(item,Actions.extension,index2+1)
            else:
                Actions.dumpToFile(code[0], Actions.extension)

    @staticmethod
    def displayExistingCodes(KEY,loadJson=False):
        lDict={}
        print "\n\nCodes with following languages were found.."
        if loadJson:
            with open(os.path.join(os.getcwd(), FilePath.CODEJSON,KEY,KEY+'.json'), 'r')as f:
                Actions.Code = json.load(f)

        for index, (key, value) in enumerate(Actions.Code.items()):
            print index + 1, "\b. ", key
            lDict[str(index+1)]=key

        l_choice = raw_input("\nEnter choice(s) of language for which you want to see the code...(separated by space): ")
        temp = l_choice.split(' ')
        for item in temp:
            if item in lDict:
                print "\n\n\n", lDict[item].capitalize(), "Code:\n"
                print "############    Total Codes found for",lDict[item],"language: ",len(Actions.Code[lDict[item]]),"    ############\n\n"
                for index2,item2 in enumerate(Actions.Code[lDict[item]]):
                    print index2+1,"\b."
                    Actions.printCode(item2)
                    print "\n\n----------------------------------------------------\n\n"
            else:
                print "Code for", item, "was not found in Language Dictionary..."
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
    python3='python3'

class XPath:
    GS_TITLE='//a[contains(@class,"gs-title")]'

class FilePath:
    CODEJSON='Codes'
    if platform=="win32":
        CHROME_DRIVERPATH = os.path.join(os.getcwd(),'Drivers/chromedriver.exe')
    elif platform == "linux" or platform == "linux2":
        CHROME_DRIVERPATH = os.path.join(os.getcwd(),'Drivers/chromedriver')

class Actions:

    ACode={}
    KEY=None
    extension=None
    LanguageDict={}

    @staticmethod
    def printCode(code):
        h=HTMLParser()
        for line in code:
            if line is not None:
                print h.unescape(line).encode('utf8')

    @staticmethod
    def initialize():
        Actions.ACode.clear()

    @staticmethod
    def register(obj):
        Actions.ACode=obj.Code
        Actions.KEY=obj.KEY

    @staticmethod
    def finalDump(f,code,extension):
        h = HTMLParser()
        for line in code:
            if line is not None:
                try:
                    f.write(str(h.unescape(line).encode('utf8')))
                except Exception as e:
                    f.write("\n@@@@ SOME ERROR ENCOUNTERED AT THIS LINE WHILE DUMPING CODE TO FILE @@@@\n\n")
                    print "\n\n#### Error in saving some code for\"", extension, "\" Kindly cross-check once with link."
                    print "#### SOME ERROR HERE HAS BEEN APPENDED IN PLACE OF IT ####"
                    print "--> HOWEVER COMPLETE CODE IS PRESENT IN JSON. YOU CAN FIND BY RUNNING \"loadCode.py\" <--\n"

    @staticmethod
    def dumpToFile(code,extension,linkText,index=None):
        if index is None:
            with open(os.path.join(os.getcwd(),FilePath.CODEJSON,Actions.KEY,linkText,Actions.KEY+extension),'w')as f:
                Actions.finalDump(f,code,extension)
        else:
            with open(os.path.join(os.getcwd(),FilePath.CODEJSON,Actions.KEY,linkText,Actions.KEY+'_'+str(index)+extension),'w')as f:
                Actions.finalDump(f,code,extension)

    @staticmethod
    def exportToFiles(linkText):
        with open(os.path.join(os.getcwd(),FilePath.CODEJSON,Actions.KEY,linkText,Actions.KEY+'.json'))as f:
            data = json.load(f)

        for index,(language,codes) in enumerate(data.items()):
            if language == Globals.python or language == Globals.python3:
                Actions.extension = '.py'
            elif language == Globals.java:
                Actions.extension = '.java'
            elif language == Globals.c:
                Actions.extension = '.c'
            else:
                Actions.extension = '.cpp'

            if len(codes)>1:
                for index2,code in enumerate(codes):
                    Actions.dumpToFile(code,Actions.extension,linkText,index2+1)
            else:
                Actions.dumpToFile(codes[0], Actions.extension,linkText)

    @staticmethod
    def displayExistingCodes(KEY,linkText,loadJson=False):
        print "Key Received : ", KEY
        print "Folder received : ",linkText

        print "\n\nCodes with following languages were found.."

        if loadJson:
            with open(os.path.join(os.getcwd(), FilePath.CODEJSON,KEY,linkText,KEY+'.json'), 'r')as f:
                Actions.ACode = json.load(f)

        for index, (key, value) in enumerate(Actions.ACode.items()):
            print index + 1, "\b. ", key
            Actions.LanguageDict[str(index+1)]=key

        l_choice = raw_input("\nEnter choice(s) of language for which you want to see the code...(separated by space) else press 'n' to continue : ")
        temp = l_choice.split(' ')
        if 'n'in temp or 'N'in temp:
            return
        for item in temp:
            if item in Actions.LanguageDict:
                print "\n\n\n", Actions.LanguageDict[item].capitalize(), "Code:\n"
                print "############    Total Codes found for",Actions.LanguageDict[item],"language: ",len(Actions.ACode[Actions.LanguageDict[item]]),"    ############\n\n"
                for index2,item2 in enumerate(Actions.ACode[Actions.LanguageDict[item]]):
                    print index2+1,"\b."
                    Actions.printCode(item2)
                    print "\n\n----------------------------------------------------\n\n"
            else:
                print "Code for", item, "was not found in Language Dictionary..."
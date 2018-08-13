import os,json
from HTMLParser import HTMLParser
from sys import platform

class Globals:
    CC_COMPLIANCE='cc-compliance'
    HREF='href'
    BASE_URL="https://www.geeksforgeeks.org/"
    SEARCH='search'
    SEARCH_BUTTON='gsc-search-button'

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

    @staticmethod
    def displayExistingCodes(KEY,loadJson=False):
        lDict={}
        print "\n\nCodes with following languages were found.."
        if loadJson:
            with open(os.path.join(os.getcwd(), FilePath.CODEJSON, KEY), 'r')as f:
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
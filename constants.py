import os,json,cgi
from HTMLParser import HTMLParser

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
    CHROME_DRIVERPATH='chromedriver.exe'

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
        print "\n\nCodes for following languages were found"
        if loadJson:
            with open(os.path.join(os.getcwd(), FilePath.CODEJSON, KEY), 'r')as f:
                Actions.Code = json.load(f)

        for index, (key, value) in enumerate(Actions.Code.items()):
            print index + 1, "\b. ", key

        l_choice = raw_input("\nEnter languages for which you want to see the code...(separated by space): ")
        temp = l_choice.split(' ')
        for item in temp:
            if item in Actions.Code:
                print "\n\n\n", item.capitalize(), "Code:\n"
                print "############    Total Codes found for",item,"language: ",len(Actions.Code[item]),"    ############\n\n"
                for index2,item2 in enumerate(Actions.Code[item]):
                    print index2+1,"\b."
                    print Actions.printCode(item2)
                    print "\n\n----------------------------------------------------\n\n"
            else:
                print "Code for", item, "was not found in Language Dictionary..."
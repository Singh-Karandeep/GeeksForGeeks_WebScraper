import json
import os
from HTMLParser import HTMLParser
from sys import platform


class Globals:
    def __init__(self):
        pass

    CC_COMPLIANCE = 'cc-compliance'
    HREF = 'href'
    BASE_URL = "https://www.geeksforgeeks.org/"
    SEARCH = 'search'
    SEARCH_BUTTON = 'gsc-search-button'
    PYTHON = 'python'
    C = 'c'
    CPP = 'cpp'
    JAVA = 'java'
    PYTHON3 = 'python3'
    PHP = 'php'
    CHASH = 'c#'


class XPath:
    def __init__(self):
        pass

    GS_TITLE = '//a[contains(@class,"gs-title")]'


class FilePath:
    def __init__(self):
        pass

    CODEJSON = 'Codes'
    if platform == "win32":
        CHROME_DRIVERPATH = os.path.join(os.getcwd(), 'Drivers/chromedriver.exe')
    elif platform == "linux" or platform == "linux2":
        CHROME_DRIVERPATH = os.path.join(os.getcwd(), 'Drivers/chromedriver')


class Actions:
    def __init__(self):
        pass

    CODE_DICT = {}
    KEY = None
    EXTENSION = None
    LANGUAGE_DICT = {}
    HTML_PARSER_OBJ = HTMLParser()

    @staticmethod
    def format_code(line):
        line = str(Actions.HTML_PARSER_OBJ.unescape(line).encode('utf8'))
        uni_line = unicode(line, 'UTF-8')
        uni_line = uni_line.replace(u"\u00A0", " ")
        return uni_line

    @staticmethod
    def initialize():
        Actions.CODE_DICT.clear()

    @staticmethod
    def register(obj):
        Actions.CODE_DICT = obj.code_dict
        Actions.KEY = obj.key

    @staticmethod
    def final_dump(f, code, extension):
        for line in code:
            if line is not None:
                try:
                    f.write(str(Actions.format_code(line)))
                except Exception as e:
                    f.write("\n@@@@ SOME ERROR ENCOUNTERED AT THIS LINE WHILE DUMPING CODE TO FILE @@@@\n\n")
                    print "\n\n#### Error in saving some code for\"", extension, "\" Kindly cross-check once with link."
                    print "#### SOME ERROR HERE HAS BEEN APPENDED IN PLACE OF IT ####"
                    print "--> HOWEVER COMPLETE CODE IS PRESENT IN JSON. YOU CAN FIND BY RUNNING \"load_code.py\" <--\n"

    @staticmethod
    def dump_to_file(code, extension, link_text, index=None):
        path = os.path.join(os.getcwd(), FilePath.CODEJSON, Actions.KEY, link_text, Actions.KEY)
        if index is not None:
            path = os.path.join(path, '_' + str(index))
        with open(path + extension, 'w')as f:
            Actions.final_dump(f, code, extension)

    @staticmethod
    def export_to_files(link_text):
        with open(os.path.join(os.getcwd(), FilePath.CODEJSON, Actions.KEY, link_text, Actions.KEY + '.json'))as f:
            data = json.load(f)

        for index, (language, code) in enumerate(data.items()):
            if language.lower().startswith(Globals.PYTHON3):
                Actions.EXTENSION = '.py'
            elif language.lower().startswith(Globals.PYTHON):
                Actions.EXTENSION = '.py'
            elif language.lower().startswith(Globals.JAVA):
                Actions.EXTENSION = '.java'
            elif language.lower().startswith(Globals.CHASH):
                Actions.EXTENSION = '.chash'
            elif language.lower().startswith(Globals.CPP):
                Actions.EXTENSION = '.cpp'
            elif language.lower().startswith(Globals.C):
                Actions.EXTENSION = '.c'
            elif language.lower().startswith(Globals.PHP):
                Actions.EXTENSION = '.php'
            else:
                Actions.EXTENSION = '.{}'.format(language.lower())

            Actions.dump_to_file(code, Actions.EXTENSION, link_text)

    @staticmethod
    def display_existing_codes(key, link_text, load_json=False):
        print "Key Received : ", key
        print "Folder received : ", link_text

        print "\n\nCodes with following languages were found.."

        if load_json:
            with open(os.path.join(os.getcwd(), FilePath.CODEJSON, key, link_text, key + '.json'), 'r')as f:
                Actions.CODE_DICT = json.load(f)

        for index, (lang, value) in enumerate(Actions.CODE_DICT.items()):
            print index + 1, "\b. ", lang
            Actions.LANGUAGE_DICT[str(index + 1)] = lang

        l_choice = raw_input("\nEnter choice(s) of language for which you want to see the code..."
                             "(separated by space) else press 'n' to continue : ")
        temp = l_choice.split(' ')
        if 'n' in temp or 'N' in temp:
            return
        for item in temp:
            if item in Actions.LANGUAGE_DICT:
                print "\n\n\n {} Code:\n".format(Actions.LANGUAGE_DICT[item].capitalize())
                print "############    Total Codes found for {} language : {}    ############\n\n".format(
                    Actions.LANGUAGE_DICT[item], len(Actions.CODE_DICT[Actions.LANGUAGE_DICT[item]]))
                for index2, item2 in enumerate(Actions.CODE_DICT[Actions.LANGUAGE_DICT[item]]):
                    print "{}.".format(index2 + 1)
                    print Actions.format_code(item2)
                    print "\n\n----------------------------------------------------\n\n"
            else:
                print "Code for {} was not found in Language Dictionary...".format(item)

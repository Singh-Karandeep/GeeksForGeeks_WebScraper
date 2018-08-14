from selenium import webdriver
import time
import requests
from BeautifulSoup import BeautifulSoup
import json
from constants import Globals,XPath,FilePath,Actions
import os
from selenium.webdriver.chrome.options import Options
import logging
from selenium.webdriver.remote.remote_connection import LOGGER

class Scrapper:

    def __init__(self):
        self.actualElements=[]
        self.KEY=None
        self.driver=None
        self.totalElements=None
        self.languages=['c','python','cpp','java','python3']
        self.titleList=None
        self.Code={}
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--log-level=3")
        self.codeFound=False

    def closePopup(self):
        count=0
        while count<=10:
            try:
                if self.driver.find_element_by_class_name(Globals.CC_COMPLIANCE):
                    self.driver.find_element_by_class_name(Globals.CC_COMPLIANCE).click()
                    break
            except Exception as e:
                pass
            time.sleep(1)
            count+=1

    def fetchSearchResults(self):
        self.titleList=self.driver.find_elements_by_xpath(XPath.GS_TITLE)

    def displayResults(self):
        print "Results found for",self.KEY,"are: "
        count = 0
        if len(self.titleList):
            for title in self.titleList:
                if len(title.text):
                    hrefLink = title.get_attribute(Globals.HREF)
                    self.actualElements.append(title)
                    print count+1,":",title.text,"   (",hrefLink,")"
                    count+=1
        self.totalElements=count
        print "Total Search Results : ", self.totalElements

    def dumpJson(self):
        if not os.path.exists(os.path.join(os.getcwd(),FilePath.CODEJSON)):
            os.mkdir(os.path.join(os.getcwd(),FilePath.CODEJSON))

        if not os.path.exists(os.path.join(os.getcwd(),FilePath.CODEJSON,self.KEY)):
            os.mkdir(os.path.join(os.getcwd(),FilePath.CODEJSON,self.KEY))

        with open(os.path.join(os.getcwd(),FilePath.CODEJSON,self.KEY,self.KEY+'.json'), 'w')as f:
            json.dump(self.Code, f, indent=4)

    def scrapeWeb(self):
        LOGGER.setLevel(logging.WARNING)
        self.driver = webdriver.Chrome(executable_path=os.path.join(os.getcwd(),FilePath.CHROME_DRIVERPATH),
                                       chrome_options=self.chrome_options)
        self.driver.get(Globals.BASE_URL)

        self.driver.find_element_by_name(Globals.SEARCH).send_keys(self.KEY)
        time.sleep(1)

        self.driver.find_element_by_class_name(Globals.SEARCH_BUTTON).click()

        self.closePopup()

        self.main_window = self.driver.current_window_handle

        self.fetchSearchResults()
        self.displayResults()
        if self.totalElements>0:
            self.scrape()

    def scrape(self):
        choice=input("Enter link to scrap: ")

        if choice<=len(self.actualElements):
            link=self.actualElements[choice-1]
            print "Trying to Scrape : ",link.text
            link.click()
            time.sleep(2)

        url=self.actualElements[choice-1].get_attribute(Globals.HREF)
        response=requests.get(url)
        html=response.content

        soup=BeautifulSoup(html)
        self.codeFound=False
        for language in self.languages:
            codes=soup.findAll('pre',attrs={'class': lambda L: L and L.startswith('brush: '+ language+';')})
            for index,code in enumerate(codes):
                code = str(code)[:-6]         #Remove </pre>
                code = code.split("\n")[1:]
                codes[index]=code

            if codes:
                self.codeFound=True
                if len(codes)>0:
                    self.Code[language]=codes

        if not self.codeFound:
            print "No C/Cpp/Python/Java code was found in the current page..."
        else:
            print "\nSaving code to:",os.path.join(os.getcwd(),FilePath.CODEJSON,self.KEY,self.KEY),'\b.json'
            self.dumpJson()
            Actions.register(self)
            Actions.exportToFiles()

    def closeSession(self):
        self.driver.switch_to.window(self.main_window)
        self.driver.close()

    def execute(self):
        self.KEY=raw_input("Enter Keyword : ")
        print "Searching for existing code for",self.KEY
        if Actions.search(self.KEY):
            print "Existing Code Files were found for",self.KEY
            Actions.displayExistingCodes(self.KEY,loadJson=True)
        else:
            print "No Code Files were found for", self.KEY,". Searching online...!!!"
            self.scrapeWeb()
            if self.codeFound:
                Actions.displayExistingCodes(None)
                choice = raw_input("Want to continue (y/n)")
                if choice == 'y' or choice == 'Y':
                    s = Scrapper()
                    s.execute()
                else:
                    print "Exiting... : )"
                    exit(1)
            else:
                while self.totalElements>0:
                    choice=raw_input("Want to continue (y/n)")
                    if choice=='y'or choice=='Y':
                        self.driver.switch_to.window(self.main_window)
                        self.displayResults()
                        if self.totalElements > 0:
                            self.scrape()
                            if self.codeFound:
                                Actions.displayExistingCodes(None)
                    else:
                        print "Exiting... : )"
                        exit(1)

if __name__=="__main__":
    s=Scrapper()
    s.execute()

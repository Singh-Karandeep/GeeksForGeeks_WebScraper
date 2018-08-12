from selenium import webdriver
import time
import requests
from BeautifulSoup import BeautifulSoup
import json
from constants import Globals,XPath,FilePath,Actions
import os
from selenium.webdriver.chrome.options import Options

class Scrapper:

    def __init__(self):
        self.actualElements=[]
        self.KEY=None
        self.driver=None
        self.totalElements=None
        self.L_languages=['c','python','cpp','java']
        self.Code={}
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")

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
        l=self.driver.find_elements_by_xpath(XPath.GS_TITLE)
        print "Results found for",self.KEY,"are: "
        count = 0
        if len(l):
            for item in l:
                if len(item.text):
                    hrefLink = item.get_attribute(Globals.HREF)
                    self.actualElements.append(item)
                    print count+1,":",item.text,"   (",hrefLink,")"
                    count+=1
        self.totalElements=count

    def dumpJson(self):
        if not os.path.exists(os.path.join(os.getcwd(),FilePath.CODEJSON)):
            os.mkdir(os.path.join(os.getcwd(),FilePath.CODEJSON))

        with open(os.path.join(os.getcwd(),FilePath.CODEJSON,self.KEY), 'w')as f:
            json.dump(self.Code, f, indent=4)

    def scrapeWeb(self):
        self.driver = webdriver.Chrome(executable_path=os.path.join(os.getcwd(),FilePath.CHROME_DRIVERPATH),chrome_options=self.chrome_options)
        self.driver.get(Globals.BASE_URL)

        self.driver.find_element_by_name(Globals.SEARCH).send_keys(self.KEY)
        time.sleep(1)

        self.driver.find_element_by_class_name(Globals.SEARCH_BUTTON).click()

        self.closePopup()

        self.main_window = self.driver.current_window_handle

        self.fetchSearchResults()

        print "Total Elements: ",self.totalElements
        choice=input("Enter link to scrap: ")

        if choice<=len(self.actualElements):
            item=self.actualElements[choice-1]
            print "Trying to Scrape : ",item.text
            item.click()
            time.sleep(2)

        url=self.actualElements[choice-1].get_attribute(Globals.HREF)
        response=requests.get(url)
        html=response.content

        soup=BeautifulSoup(html)
        self.codeFound=False
        for item in self.L_languages:
            code=soup.findAll('pre',attrs={'class': lambda L: L and L.startswith('brush: '+ item)})
            for index,item2 in enumerate(code):
                item2 = str(item2)[:-6]         #Remove </pre>
                item2 = item2.split("\n")[1:]
                code[index]=item2

            if code:
                self.codeFound=True
                if len(code)>0:
                    self.Code[item]=code

        if not self.codeFound:
            print "No C/Cpp/Python/Java code was found in the current page..."
        else:
            print "Saving code to:",FilePath.CODEJSON,"/",self.KEY
            self.dumpJson()
            Actions.register(self)

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
            self.closeSession()

if __name__=="__main__":
    s=Scrapper()
    s.execute()

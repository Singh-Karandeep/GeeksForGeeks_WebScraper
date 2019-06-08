import json
import logging
import os
import time

import requests
from BeautifulSoup import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.remote_connection import LOGGER

from constants import Globals, XPath, FilePath, Actions


class Scrapper:

    def __init__(self):
        self.actual_elements = []
        self.key = None
        self.total_elements = None
        self.title_list = None
        self.code_dict = {}
        self.code_found = False
        self.link_text = None
        self.special_characters = ['<', '>', ':', '\"', '/', '\\', '|', '?', '*', '.']

        self.driver = None
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--log-level=3")

    def close_popup(self):
        count = 0
        while count <= 10:
            try:
                compliance_element = self.driver.find_element_by_class_name(Globals.CC_COMPLIANCE)
                if compliance_element:
                    compliance_element.click()
                    break
            except Exception as e:
                pass
            time.sleep(1)
            count += 1

    def fetch_search_results(self):
        self.title_list = self.driver.find_elements_by_xpath(XPath.GS_TITLE)

    def display_results(self):
        print "Results found for {} are : ".format(self.key)
        count = 0
        if self.title_list:
            for title in self.title_list:
                if title.text:
                    href_link = title.get_attribute(Globals.HREF)
                    self.actual_elements.append(title)
                    print "{} : {} ({})".format(count + 1, title.text.encode('utf8'), href_link.encode('utf8'))
                    count += 1
        self.total_elements = count
        print "Total Search Results : {}".format(self.total_elements)

    @staticmethod
    def make_dir(path):
        if not os.path.exists(path):
            os.mkdir(path)

    def dump_json(self):
        for character in self.special_characters:
            self.link_text = self.link_text.replace(character, '_')

        json_path = os.path.join(os.getcwd(), FilePath.CODEJSON)
        Scrapper.make_dir(json_path)

        key_folder = os.path.join(os.getcwd(), FilePath.CODEJSON, self.key)
        Scrapper.make_dir(key_folder)

        link_folder = os.path.join(os.getcwd(), FilePath.CODEJSON, self.key, self.link_text)
        Scrapper.make_dir(link_folder)

        with open(os.path.join(link_folder, self.key + '.json'), 'w')as f:
            json.dump(self.code_dict, f, indent=4)

    def scrape_web(self):
        LOGGER.setLevel(logging.WARNING)
        self.driver = webdriver.Chrome(executable_path=FilePath.CHROME_DRIVERPATH,
                                       chrome_options=self.chrome_options)
        self.driver.get(Globals.BASE_URL)

        self.driver.find_element_by_name(Globals.SEARCH).send_keys(self.key)
        time.sleep(1)

        self.driver.find_element_by_class_name(Globals.SEARCH_BUTTON).click()

        self.close_popup()

        self.main_window = self.driver.current_window_handle

        self.fetch_search_results()
        self.display_results()
        if self.total_elements > 0:
            self.scrape()

    @staticmethod
    def fill_language(languages, codes):
        if len(languages) == len(codes):
            return
        else:
            print "Language for code could not be detected. Saving in Text format."
            for _ in codes:
                languages.append('Text')

    def scrape_code_in_page(self, soup):
        languages = []
        for hit in soup.findAll(attrs={'class': 'tabtitle'}):
            languages.append(''.join(hit.findAll(text=True)))

        codes = []
        for hit in soup.findAll(attrs={'class': 'code'}):
            codes.append(''.join(hit.findAll(text=True)))
            # content = hit.contents[1]
            # for line in content:
            #     if type(line)!=NavigableString:
            #         print line.text
            # print "\n#####################################\n"

        Scrapper.fill_language(languages, codes)

        for language, code in zip(languages, codes):
            if language not in self.code_dict:
                self.code_dict[language] = []
            self.code_dict[language].append(code)
            self.code_found = True

    def scrape(self):
        choice = input("Enter link to scrap: ")
        if choice <= len(self.actual_elements):
            link = self.actual_elements[choice - 1]
            print "Trying to Scrape : {}".format(link.text)
            self.link_text = link.text
            link.click()
            time.sleep(2)

            url = link.get_attribute(Globals.HREF)
            response = requests.get(url)
            html = response.content

            soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)

            self.code_found = False

            self.scrape_code_in_page(soup)

            if not self.code_found:
                print "No C/Cpp/Python/Java code was found in the current page..."
            else:
                print "\nSaving code to : {}.json".format(
                    os.path.join(os.getcwd(), FilePath.CODEJSON, self.key, self.link_text,
                                 self.key))
                self.dump_json()
                Actions.register(self)
                Actions.export_to_files(self.link_text)
        else:
            print "Please enter valid choice..."
            self.scrape()

    def close_session(self):
        self.driver.switch_to.window(self.main_window)
        self.driver.close()

    @staticmethod
    def get_link_text(key_code, code_list):
        for index, (key, link) in enumerate(code_list):
            if str(key) == str(key_code):
                return link
        return None

    def continue_further(self):
        print "Continue for: \n1. {}\n2. New keyword\n3. Exit".format(self.key)

        choice = input("Enter your choice: ")
        if choice == 1:
            self.driver.switch_to.window(self.main_window)
            self.display_results()
            if self.total_elements > 0:
                self.code_dict.clear()
                self.scrape()
                if self.code_found:
                    Actions.display_existing_codes(self.key, self.link_text)
        elif choice == 2:
            Actions.initialize()
            self.code_dict.clear()
            Scrapper().main()
        elif choice == 3:
            print "Exiting... :)"
            exit(2)

    def main(self):
        self.key = raw_input("Enter Keyword to scrape from https://geeksforgeeks.org: ")
        print "Searching for existing code for {}.\n\nNote : All Scraped Codes will " \
              "be saved under Codes/ Directory\n\n".format(self.key)
        continue_execution = True
        if os.path.exists(os.path.join(FilePath.CODEJSON, self.key)):
            code_list = []
            code_directory = os.listdir(os.path.join(FilePath.CODEJSON, self.key))
            if len(code_directory) > 0:
                print "Existing Code Folders were found for", self.key, ":"
            for index, item in enumerate(code_directory):
                print "{}. {}".format(index + 1, item)
                code_list.append([index + 1, item])
            choice = raw_input('Enter index to display codes else press \'n\' to search for new codes...')
            if choice.lower() != 'n':
                self.link_text = Scrapper.get_link_text(choice, code_list)
                if self.link_text is None:
                    print "Invalid option supplied..."
                else:
                    Actions.display_existing_codes(self.key, self.link_text, load_json=True)
                    print "Please use load_code.py to further explore already saved Codes."
                    continue_execution = False
            else:
                continue_execution = True

        if continue_execution:
            print "No Code Files were found for {}. Searching online...!!!".format(self.key)
            self.scrape_web()
            if self.code_found:
                Actions.display_existing_codes(self.key, self.link_text)
            while self.total_elements > 0:
                choice = raw_input("Want to continue (y/n)")
                if choice.lower() == 'y':
                    self.continue_further()
                else:
                    print "Exiting... :)"
                    exit(1)


if __name__ == "__main__":
    Scrapper().main()

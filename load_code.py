import os

from constants import Actions, FilePath


class LoadCode:
    def __init__(self):
        self.sorted_codes = None
        self.link_text = []
        self.code_directory = []
        self.key = None

    @staticmethod
    def is_number(s):
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

    @staticmethod
    def get_link_text(key_code, code_list):
        for index, (key, link) in enumerate(code_list):
            if str(key) == str(key_code):
                return link
        return None

    def check_exceptions(self, choice):
        if LoadCode.is_number(choice):
            key_code = int(choice)
            if key_code > len(self.code_directory) or key_code <= 0:
                print "Enter a valid range"
                exit(1)
            return choice
        else:
            print "Only digits allowed..."
            exit(2)

    def main(self):
        continue_further = True
        while continue_further:
            if os.path.exists(FilePath.CODEJSON):
                code_list = []
                self.code_directory = os.listdir(os.path.join(FilePath.CODEJSON))
                if len(self.code_directory) > 0:
                    print "Existing Code Folders were found for"
                else:
                    print "No Code Directories were found"
                for index, item in enumerate(self.code_directory):
                    print "{}. {}".format(index + 1, item)
                    code_list.append([index + 1, item])
                choice = raw_input('Enter Folder Option to load Code Files: ')

                self.check_exceptions(choice)

                self.key = LoadCode.get_link_text(choice, code_list)
                self.code_directory = os.listdir(os.path.join(FilePath.CODEJSON, self.key))
                if len(self.code_directory) > 0:
                    code_list = []
                    for index, item in enumerate(self.code_directory):
                        print index + 1, "\b.", item
                        code_list.append([index + 1, item])
                    choice = raw_input("Choose Code File to open: ")
                    self.check_exceptions(choice)
                    self.link_text = LoadCode.get_link_text(choice, code_list)
                    Actions.display_existing_codes(self.key, self.link_text, load_json=True)
                    choice = raw_input('Want to Continue (y/n):')
                    if choice.lower() == 'n':
                        continue_further = False
                else:
                    print "No Code Directories were found inside", self.key
                    continue_further = False
            else:
                print "Codes directory doesn't exists..."
                continue_further = False


if __name__ == "__main__":
    LoadCode().main()

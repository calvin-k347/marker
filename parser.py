import re
class Parser:
    patterns = {
        "heading": r"#{1,3}+(.+)",
        "lines": r"-{3}|\*{3}|_{3}"
    }
    def __init__(self, file):
        self.file = file
        self.content = ""
    def __read(self):
        with open(self.file) as f:
            for line in f:
                self.content += line
    def __parse(self):
        h = re.findall(self.patterns['heading'], self.content)
        l = re.findall(self.patterns['lines'], self.content)
        print(h)
        print(l)
    def method(self):
        self.__read()
        self.__parse()
class Parser:
    def __init__(self, file):
        self.file = file
        self.contents = []
    def __read(self):
        with open(self.file) as f:
            for line in f:
                self.contents.append(line)
        print(self.contents)
    def method(self):
        self.__read()
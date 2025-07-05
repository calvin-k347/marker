import re
class Parser:
    patterns = {
        "heading": re.compile("#{1,3}+(.+)"),
        "lines": re.compile(r"-{3}|\*{3}|_{3}"),
        "bold": re.compile(r"\*\*(.+?)\*\*")
    }
    boiler_plate = '''
<!DOCTYPE html>
<html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    
</body>
</html>
''' 
    def __init__(self, file):
        self.file = file
        self.content = ""
    def __read(self):
        with open(self.file) as f:
            for line in f:
                self.content += line
    def __parse(self):
        h = re.findall(Parser.patterns['heading'], self.content)
        l = re.findall(self.patterns['lines'], self.content)
        b = re.findall(self.patterns['bold'], self.content)
        convert = ""
        contained = False
        for i in range(len(self.content)):
            if not contained:
                #check if matches heading regex
                heading = Parser.patterns['heading'].match(self.content[i:])
                if heading:
                    depth = heading.group().count("#")
                    html_heading = f'''<h{depth}>\n{heading.group()[depth:]}\n<h{depth}>
                    '''
                    print(html_heading)
                    contained = True
                    continue
                line = Parser.patterns['lines'].match(self.content[i:])
                if line:
                    print(line)
                    contained = True
                    continue
                



        convertion = Parser.boiler_plate[0:190] + convert + Parser.boiler_plate[190:]
        with open("new.html", "w") as f:
            pass
        #print(h)
        #print(l)
        #print(b)
        #print(convertion)
    def method(self):
        self.__read()
        self.__parse()
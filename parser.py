import re
class Parser:
    patterns = {
        "heading": re.compile(r"#{1,3}+(.+)"),
        "lines": re.compile(r"-{3}|\*{3}|_{3}"),
        "text_styles": re.compile(r"\*(.+)\*|\*\*(.+)\*\*|\*\*\*(.+)\*\*\*")
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
        convert = ""
        contained = False
        buffer = 0
        curr_pg = ""
        for i in range(len(self.content)):
            if not contained:
                #check if matches heading regex
                heading = Parser.patterns['heading'].match(self.content[i:])
                line = Parser.patterns['lines'].match(self.content[i:])
                styled = Parser.patterns['text_styles'].match(self.content[i:])
                if heading or line or (heading == None and line == None and i == len(self.content) - 1 ):
                    html_paragraph = f"<p>\n{curr_pg}\n</p>"
                    convert += html_paragraph
                    print(html_paragraph)
                    curr_pg = ""
                    contained = True
                if heading:
                    depth = heading.group().count("#")
                    heading_txt = heading.group()[depth:]
                    #print(f"\n my depth is {depth} and my text is {heading_txt}. this comes from {heading.group()}")
                    buffer = depth + len(heading_txt)
                    html_heading = f'''<h{depth}>\n{heading_txt}\n</h{depth}>
                    '''
                    print(html_heading)
                    convert += html_heading
                    contained = True
                    continue
                elif line:
                    buffer = 3
                    html_line = "<div class=\"lineclass\"></div>"
                    print(html_line)
                    convert += html_line
                    contained = True
                    continue
                elif styled and not line:
                    depth = styled.group().count("*")
                    styled_txt  = styled.group()[depth//2:len(styled.group())-depth//2]
                    buffer = depth + len(styled_txt)
                    html_styled = f'''<span>\n{styled_txt}\n</span>'''
                    print(html_styled)
                    convert += html_styled
                    contained = True
                    continue
                else:
                    curr_pg += self.content[i]
            else:
                #print(f"buffer is: {buffer}, char is {self.content[i]}")
                if buffer > 1:
                    buffer -= 1
                else:
                    contained = False
        convertion = Parser.boiler_plate[0:190] + convert + Parser.boiler_plate[190:]
        with open("new.html", "w") as f:
            f.write(convertion)
        #print(h)
        #print(l)
        #print(b)
        #print(convertion)
    def method(self):
        self.__read()
        self.__parse()
import re, os
class Parser:
    patterns = {
        "heading": re.compile(r"#{1,3}+(.+)"),
        "lines": re.compile(r"-{3}|\*{3}|_{3}"),
        "text_styles": re.compile(r"\*(.+)\*|\*\*(.+)\*\*|\*\*\*(.+)\*\*\*"),
        "new_line": re.compile(r"\n\n"),
        "center": r"\c",
        "red": r"\r",
        "blue": r"\b",
    }

    boiler_plate = '''
<!DOCTYPE html>
<html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="./output.css" rel="stylesheet">
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
                nl = Parser.patterns['new_line'].match(self.content[i:])
                if heading or line or nl or (heading == None and line == None and i == len(self.content) - 1 ) and curr_pg != "":
                    html_paragraph = f"<p>\n{curr_pg}\n</p>"
                    if nl:
                        html_paragraph += "<br></br>"
                    convert += html_paragraph
                    print(html_paragraph)
                    curr_pg = ""
                    contained = True
                if heading:
                    depth = heading.group().count("#")
                    heading_txt = heading.group()[depth:]
                    if depth == 1:
                        style = "text-2xl"
                    elif depth == 2:
                        style = "text-xl"
                    else:
                        style = "text-lg"

                    #print(f"\n my depth is {depth} and my text is {heading_txt}. this comes from {heading.group()}")
                    buffer = depth + len(heading_txt)
                    html_heading = f'''<h{depth} class="{style}">\n{heading_txt}\n</h{depth}>
                    '''
                    convert += html_heading
                    contained = True
                    continue
                elif line:
                    buffer = 4
                    html_line = "<div class=\"lineclass\"></div>"
                    convert += html_line
                    contained = True
                    continue
                elif styled and not line:
                    depth = styled.group().count("*") // 2
                    
                    styled_txt  = styled.group()[depth:len(styled.group())-depth]
                    buffer = len(styled.group())
                    if depth == 1:
                        style = "italic"
                    elif depth == 2:
                        style = "font-bold"
                    elif depth == 3:
                        style = "italic font-bold"
                    html_styled = f'''\n\t<span class="{style}">\n{styled_txt}\n</span>\n'''
                    if curr_pg == "":
                        convert+= html_styled
                    else:
                        curr_pg += html_styled
                    contained = True
                else:
                    curr_pg += self.content[i]
            else:
                #print(f"buffer is: {buffer}, char is {self.content[i]}")
                if buffer > 1:
                    buffer -= 1
                else:
                    contained = False
        convertion = Parser.boiler_plate[0:238] + convert + Parser.boiler_plate[238:]
        with open("new.html", "w") as f:
            f.write(convertion)
        with open("input.css", "w") as f:
            f.write("@import \"tailwindcss\";")
        return (os.getcwd() +r"\new.html")
    def method(self):
        self.__read()
        return self.__parse()
        
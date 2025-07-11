import re, os
class Parser:
    patterns = {
        "heading": re.compile(r"#{1,3}+(.+)"),
        "lines": re.compile(r"-{3}|_{3}"),
        "text_styles": re.compile(r"\*\*\*(.+)\*\*\*|\*\*(.+)\*\*|\*(.+)\*"),
        "new_line": re.compile(r"\n\n"),
        "formats": re.compile(r"t"),
        "img": re.compile(r"![image](.+)"),
        "list": re.compile(r"-{1} .+"),
        "code": re.compile(r"`.+`")
    }

    boiler_plate_top = '''
<!DOCTYPE html>
<html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="../static/styles/output.css" rel="stylesheet">
    <title>Document</title>
</head>
<body>
''' 
    boiler_plate_bottom = '''
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
    def __parse(self, n):
        convert = '''\t<div class="grid mt-5 md:w-1/2  md:mx-auto justify-center items-center">\n\t'''
        contained = False
        buffer = 0
        curr_pg = ""
        listed = False
        for i in range(len(self.content)):
            if self.content[i] == "\n":
                print("NL")
            else:
                print(self.content[i])
            #print(curr_pg)
            if not contained:
                #check if matches heading regex
                heading = Parser.patterns['heading'].match(self.content[i:])
                line = Parser.patterns['lines'].match(self.content[i:])
                styled = Parser.patterns['text_styles'].match(self.content[i:])
                nl = Parser.patterns['new_line'].match(self.content[i:])
                image = Parser.patterns['img'].match(self.content[i:])
                listing = Parser.patterns['list'].match(self.content[i:])
                code = Parser.patterns['code'].match(self.content[i:])
                if heading or line or nl or ( i == len(self.content) - 1 ):
                    if curr_pg != "":
                        html_paragraph = f'''<p class="p-2">\n{curr_pg}\n</p>''' if not listed else f'''{curr_pg} </li>'''
                        listed = False
                        if nl:
                            html_paragraph += "<br>"
                        convert += html_paragraph
                        print(html_paragraph)
                        curr_pg = ""
                        buffer = 0
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
                    buffer = len(heading.group())-1
                    html_heading = f'''<h{depth} class="{style} {"text-center" if depth == 1 else ""}">\n{heading_txt}\n</h{depth}>
                    '''
                    convert += html_heading
                    print(html_heading)
                    contained = True
                    continue
                elif line:
                    buffer = len(line.group()) -1
                    html_line = f"<div class=\"w-full border-dotted border-b-4 mt-2 mb-2\"></div>"
                    convert += html_line
                    print(html_line)
                    contained = True
                    continue
                elif styled and not line:
                    depth = styled.group().count("*") // 2
                    
                    styled_txt  = styled.group()[depth:len(styled.group())-depth]
                    
                    if depth == 1:
                        style = "italic"
                    elif depth == 2:
                        style = "font-bold"
                    elif depth == 3:
                        style = "italic font-bold"
                    html_styled = f'''\n\t<span class="{style}">\n{styled_txt}\n</span>\n'''
                    
 
                    curr_pg += html_styled
                    buffer = len(styled.group()) -2
                    print("styled curr pg: ", curr_pg)
                    contained = True
                elif image:
                    url = image.group()[image.group().index("[")+1:image.group().index("]")]
                    html_img = f'''<div class="w-50 h-50 mx-auto my-2"><img class="w-full h-full object-contain" src="{url}" alt="alr"></div>'''
                    convert += html_img
                    buffer += len(image.group()) -1
                    contained = True
                elif listing:
                    li = listing.group()[1:]
                    
                    if "*" in li:
                        buffer += li.index("*")
                        curr_pg += '''<li class="ml-4">'''

                    else:
                        buffer += len(li)
                        curr_pg += '''<li class="ml-4">'''
                    listed = True

                elif code:
                    indent = f"ml-{code.group().count("\t") *2}"


                    convert += f'''<div class="w-full bg-gray-200"><p class="font-mono p-2">{code.group()[1:-1]}</p></div>'''
                    buffer += len(code.group()) - 1 
                    contained = True
                else:
                    curr_pg += self.content[i]
            else:
                print(f"buffer is: {buffer}, char is {self.content[i]}")
                if buffer >= 1: 
                    buffer -= 1
                else:
                    if curr_pg and i == len(self.content) -1:
                        convert += f'''<p class="">{curr_pg}</p>'''
                    contained = False
        convert  += '''</div>'''
        convertion = Parser.boiler_plate_top + convert + Parser.boiler_plate_bottom
        try:
            os.mkdir("templates")
            os.makedirs("static/styles")
        except FileExistsError:
            pass
        with open(f"templates/new{n}.html", "w") as f:
            f.write(convertion)
        with open("static/styles/input.css", "w") as f:
            f.write("@import \"tailwindcss\";")
        return (os.getcwd() +f"\\templates\\new{n}.html")
    def method(self, num):
        self.__read()
        return self.__parse(num)
        
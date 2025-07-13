import re, os
from lexer import Lexer
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
    heading_styles = {1: "text-2xl",
                      2: "text-xl",
                      3:"text-lg"}
    emphasis_styles = {1: "italic",
                      2: "font-bold",
                      3:"italic font-bold"}
    boiler_plate_top = '''
<!DOCTYPE html>
<html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="../static/styles/output.css" rel="stylesheet">
    <title>Document</title>
</head>
<body class="w-full h-full">
''' 
    boiler_plate_bottom = '''
</body>
</html>
    '''
    def __init__(self, file):
        self.file = file
        self.content = ""
        self.stack = []
        self.states = {
        "heading": False,
        "emphasis": False,
        "paragraph": False,
        "code": False, 
        "list-item": False,
        "line": False,
        "break": False
    }
    def __inline(self, text):
        #TODO: check for inline styles 
        return text
    def __parse(self, n):
        convert = '''\t<div class="grid sm:w-4/5 md:w-1/2 mx-auto mt-5  items-center">\n\t'''
        lexed = Lexer(self.file).lex()
        curr_pg = ""
        for i, token in enumerate(lexed):
            print(token)

            self.states[token.type] = True
            if token.type not in ["paragraph", "emphasis"] and curr_pg:
                curr_pg += '''</p>'''
                convert += curr_pg
                curr_pg = ""
            if self.states["heading"]:
                token.value = self.__inline(token.value)
                convert += f'''<h{token.level} class="{Parser.heading_styles[token.level]}">{token.value}</h{token.level}>'''
            if self.states["line"]:
                convert += f"<div class=\"w-full border-dotted border-b-4 mt-2 mb-2\"></div>"
            if self.states["list-item"]:
                convert += f'''<li class="ml-4">{self.__inline(token.value)}</li>''' 
            if self.states["code"]:
                convert += f'''<div class="w-full bg-gray-200"><p class="font-mono p-2">{token.value}</p></div>'''
            if self.states["paragraph"]:
                if "<p>" in curr_pg:
                    curr_pg += f''' {token.value}'''
                else:
                    curr_pg += f'''<p> {token.value}'''
            if self.states["emphasis"]:
                curr_pg += f'''<span class="{Parser.emphasis_styles[token.level]}">{token.value}</span>'''
            if self.states["break"]:
                convert += "<br>"
            self.states[token.type] = False
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
        return self.__parse(num)
        
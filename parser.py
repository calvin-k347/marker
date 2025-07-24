import re, os
from lexer import Lexer
from mdtoken import Token
class Parser:
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
        self.states = {
        "heading": False,
        "emphasis": False,
        "paragraph": False,
        "code": False, 
        "list-item": False,
        "line": False,
        "break": False,
        "image":False,
        "multi-line-code": False, 
        "div": False
    }
        self.active_states = set()
    def __inline(self, text):
        text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<span class="italic font-bold">\1</span>', text)
        text = re.sub(r'\*\*(.+?)\*\*', r'<span class="font-bold">\1</span>', text)
        text = re.sub(r'\*(.+?)\*', r'<span class="italic">\1</span>', text)
        text = re.sub(r'`(.+?)` | ```(.+?)```', r'<div class="w-full bg-gray-200"><p class="font-mono p-2">\1</p></div>', text)
        return text
    def __parse(self, n):
        convert = '''\t<div class="grid sm:w-4/5 md:w-1/2 mx-auto mt-5  items-center">\n\t'''
        lexed = Lexer(self.file).lex()
        curr_pg = ""
        style = None
        for i, token in enumerate(lexed):
            if token.type == "heading":
                self.parse_heading(token)
            elif token.type == "paragraph":
                self.parse_paragraph(token)
            elif token.type == "emph":
                self.parse_emph(token)
            elif token.type == "code":
                self.parse_code(token)
            elif token.type == "img":
                self.parse_img(token)
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
        
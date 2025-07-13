from mdtoken import Token
import re
class Lexer:
    operators = ["#", "-", "`", "\n", "*"]
    def __init__(self, file):
        self.file = file
    def lex(self):
        literal_reg = ""
        q = []
        with open(self.file) as f:
            for line in f:
                stripped_line = line[:-1]
                if not stripped_line:
                    q.append(Token("break", ""))
                else:
                    start = stripped_line[0]
                    match start:
                        case "#":
                            depth = stripped_line.count("#")
                            token = Token("heading", stripped_line[depth:], level=depth)
                            q.append(token)
                        case "-":
                            if stripped_line == "---":
                                token = Token("line", "---")
                            elif len(stripped_line) > 2 and stripped_line[0:2] == "- ":
                                token = Token("list-item", stripped_line[stripped_line.index("-"):])
                            q.append(token)
                        case "":
                            q.append(Token("break", ""))
                        case _:
                            buffer = 0
                            for i, char in enumerate(line):
                                if buffer:
                                    buffer -=1 
                                    continue
                                if char not in ["*", "`", "\n"]:
                                    literal_reg += char
                                elif char == "*":
                                    emph = re.search(r"\*\*\*(.+)\*\*\*|\*\*(.+)\*\*|\*(.+)\*", stripped_line)
                                    if emph:
                                        depth = emph.group().count("*")
                                        if literal_reg:
                                            q.append(Token("paragraph",literal_reg))
                                            literal_reg = ""
                                        q.append(Token("emphasis", emph.group()[depth//2:-depth//2], level=depth//2))
                                        buffer += len(emph.group())
                                    else:
                                        literal_reg += char
                                elif char == "`":
                                    code = re.search(r"`.+`", stripped_line[stripped_line.index("`"):])
                                    if code:
                                        if literal_reg:
                                            q.append(Token("paragraph", literal_reg))
                                            literal_reg = ""
                                        q.append(Token("code", code.group()[1:-1]))
                                        buffer += len(code.group()) -1
                            if literal_reg:
                                q.append(Token("paragraph", literal_reg))
                                literal_reg = ""
        for t in q:
            print(t)

                            
                                


                
                        
                
if __name__ == "__main__":
    l = Lexer("test4.md")
    l.lex()
    t = "- things"
    print(t[0:1])
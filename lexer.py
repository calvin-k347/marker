from mdtoken import Token
import re
class Lexer:
    operators = ["#", "-", "`", "\n", "*"]
    def __init__(self, file):
        self.file = file
    def lex(self):
        literal_reg = ""
        q = []
        multi_line = False
        with open(self.file) as f:
            for line in f:
                stripped_line = line[:-1] if line[-1] == "\n"  else line
                if not stripped_line:
                    q.append(Token("break", ""))
                elif not multi_line:
                    start = stripped_line[0]
                    match start:
                        case "#":
                            depth = stripped_line.count("#")
                            token = Token("heading", stripped_line[depth:], level=depth)
                            q.append(token)
                        case "-" | "_" | "+":
                            if stripped_line in ["---", "___"]:
                                token = Token("line", start*3)
                            elif len(stripped_line) > 2 and stripped_line[0:2] in ["- ", "+ "]:
                                token = Token("list-item", stripped_line[1:], "UNORDERED" if start == "-" else "ORDERED")
                            q.append(token)
                        case "":
                            q.append(Token("break", ""))
                        case _:
                            buffer = 0
                            for i, char in enumerate(line):
                                if buffer:
                                    buffer -=1 
                                    continue
                                if char not in ["*", "`", "\n", "!", "<"]:
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
                                    if len(stripped_line) > 2 and stripped_line[0:3] == "```":

                                        value = stripped_line[3:-3] if stripped_line[-3:-1] == "```" else stripped_line[3:]
                                        if stripped_line[-3:] == "```":
                                            q.append(Token("code", stripped_line[3:-3]))
                                            buffer = len(stripped_line) -1
                                        else:
                                            q.append(Token("multi-line-code", stripped_line[3:]))
                                        if literal_reg:
                                            q.append(Token("paragraph", literal_reg))
                                            literal_reg = ""
                                         
                                    elif (code :=re.search(r"`.+`", stripped_line[stripped_line.index("`"):])):
                                        if literal_reg:
                                            q.append(Token("paragraph", literal_reg))
                                            literal_reg = ""
                                        q.append(Token("code", code.group()[1:-1]))
                                        buffer += len(code.group()) -1
                                elif char == "!":
                                    if (img := re.match(r"!\[(.*?)\]\((.*?)\)", stripped_line)):
                                        alt = img.group()[img.group().index("[")+1: img.group().index("]")]
                                        url = img.group()[img.group().index("(")+1: img.group().index(")")]
                                        q.append(Token("image",[alt,url]))
                                        buffer += len(img.group()) -1
                                    else:
                                        literal_reg += "!"
                                elif char == "<":
                                    if len(stripped_line) > 1 and stripped_line[i: i+1] == "<>":
                                        q.append(Token("div", None))
                                        buffer +=1
                                    elif len(stripped_line) > 2 and stripped_line[i:i+2] == "</>":
                                        q.append(Token("div", None))
                                        buffer += 2
                                    else:
                                        literal_reg += "<"
                            if literal_reg:
                                q.append(Token("paragraph", literal_reg))
                                literal_reg = ""
        print(q)
        return q

                            
                                

                
                        
                
if __name__ == "__main__":
    l = Lexer("test4.md")
    l.lex()
from mdtoken import Token
class Lexer:
    operators = ["#", "-", "`", "\n", "*"]
    def __init__(self, file):
        self.file = file
        self.q = []
        self.literal_reg = ""
    def lex(self):
        with open(self.file) as f:
            token = None
            for line in f:
                for char in line:              
                    if char in Lexer.operators:
                        if token:
                            self.q.append(token)
                        token = Token(char, None)
                    else:
                        token.add_value(char)
            self.q.append(token)
        return self.q
if __name__ == "__main__":
    l = Lexer("test4.md")
    l.lex()
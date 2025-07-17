class Token:
    MULTI_LINE_TOKENS = {"list-item"}
    VALID_TOKENS = {"heading",
                    "paragraph",
                    "emphasis", 
                    "list-item", 
                    "code", 
                    "image", 
                    "line", 
                    "break",
                    "multi-line-code",
                    "div"}
    def __init__(self, type, value, level = None):
        self.type = type if type in Token.VALID_TOKENS else "INVALID TOKEN"
        self.value = value
        self.level = level
    def __repr__(self):
        return f"[{self.type if self.type != "\n" else "NL"}, {self.value} {"," + str(self.level) if self.level else ""}]"
        
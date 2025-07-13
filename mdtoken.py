class Token:
    def __init__(self, type, value, level = None):
        self.type = type
        self.value = value
        self.level = level
    def __repr__(self):
        return f"[{self.type if self.type != "\n" else "NL"}, {self.value} {"," + str(self.level) if self.level else ""}]"
        
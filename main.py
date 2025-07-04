import re, sys
from parser import Parser
print("hello world")

for arg in sys.argv[1:]:
    p = Parser(arg)
    p.method()

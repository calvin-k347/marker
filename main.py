import sys
from parser import Parser
for arg in sys.argv[1:]:
    p = Parser(arg)
    p.method()

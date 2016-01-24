import sys
import ast
from unparse import Unparser

SOURCE = """
def foo():
    print "hello", "world"

foo()
"""

class Capitalizer(ast.NodeTransformer):

    def visit_Str(self, node):
        node.s = node.s.capitalize()
        return node

if __name__ == "__main__":
    print "---origin source---"
    print SOURCE
    tree = ast.parse(SOURCE)
    Capitalizer().visit(tree)
    print "---modified source---"
    Unparser(tree, sys.stdout)
    print
    print "---run the new source---"
    eval(compile(tree, "", "exec"))

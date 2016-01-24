import sys
import ast
from unparse import Unparser
import os

class InvocationLogger(ast.NodeTransformer):

    def visit_FunctionDef(self, node):
        node.body.insert(0,
            ast.Print(dest=None, values=[ast.Str("--before call: " + node.name,
                    lineno=node.lineno, col_offset=node.col_offset)],
                    nl=True, lineno=node.lineno, col_offset=node.col_offset))
        node.body.append(
            ast.Print(dest=None, values=[ast.Str("--after call:" + node.name,
                    lineno=node.lineno, col_offset=node.col_offset)],
                    nl=True, lineno=node.lineno, col_offset=node.col_offset))
        return node


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "usage: python {} <source_file>".format(sys.argv[0])
        exit()

    filename = sys.argv[1]
    if (not os.path.exists(filename)):
        print "'{}' does not exist!".format(filename)

    with open(filename) as f:
        tree = ast.parse(f.read())
        InvocationLogger().visit(tree)
        output_file = "logged_" + filename
        with open(output_file, 'wb') as f_out:
            Unparser(tree, f_out)
            print "write generated code into {}".format(output_file)
        eval(compile(tree, "", "exec"))


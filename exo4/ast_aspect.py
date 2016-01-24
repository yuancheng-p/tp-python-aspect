import sys
import ast
from unparse import Unparser
import os

class InvocationLogger(ast.NodeTransformer):

    def visit_Expr(self, node):
        print 'expr'
        if isinstance(node.value, ast.Call):
            print "call: " + node.value.func.id
            before_node, after_node = self.make_around_nodes(node.value.func.id, node.lineno, node.col_offset)
            return [before_node, node, after_node]
        return node

#    def visit_Call(self, node):
#        fn_name = None
#        if isinstance(node.func, ast.Name):
#            print 'visit call with Name:', node.func.id
#            fn_name = node.func.id
#        elif isinstance(node.func, ast.Attribute):
#            print 'visit call with Attribute:', node.func.value.s
#            fn_name = node.func.value.s
#        if fn_name:
#            before_node, after_node = self.make_around_nodes(fn_name, node.lineno, node.col_offset)
#            return [before_node, node, after_node]
#        return node

    def make_around_nodes(self, fn_name, lineno, col_offset):
        before_node  = ast.Print(dest=None, values=[ast.Str("--before call:" + fn_name,
                lineno=lineno, col_offset=col_offset)],
                nl=True, lineno=lineno, col_offset=col_offset)
        after_node  = ast.Print(dest=None, values=[ast.Str("--after call:" + fn_name,
                lineno=lineno, col_offset=col_offset)],
                nl=True, lineno=lineno, col_offset=col_offset)
        return before_node, after_node


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "usage: python {} <source_file>".format(sys.argv[0])
        exit()

    filename = sys.argv[1]
    if (not os.path.exists(filename)):
        print "'{}' does not exist!".format(filename)

    with open(filename) as f:
        tree = ast.parse(f.read())
        print '----------------'
        print ast.dump(tree)
        print '----------------'
        InvocationLogger().visit(tree)
        print '----------------'
        Unparser(tree)
#        output_file = "logged_" + filename
#        with open(output_file, 'wb') as f_out:
#            Unparser(tree)
#            print "write generated code into {}".format(output_file)
        print
        print '----------------'
        eval(compile(tree, "", "exec"))

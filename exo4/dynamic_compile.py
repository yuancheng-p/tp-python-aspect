import sys
import ast
from unparse import Unparser


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        exit()

    tree = ast.parse(sys.argv[1])
    print ast.dump(tree)
    Unparser(tree, sys.stdout)
    print

ast.parse(...) and eval(...) of the ast module
==============================================

Dynamic compilation
-------------------

``ast.parse()`` can parse a Python source into an AST node.
Let's write a script that parses source read from terminal,
then we print the AST, and the formated source code using ``unparse.py``::

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


save it as `dynamic_compile.py <exo4/dynamic_compile.py>`_ and run it::

  $> python dynamic_compile.py "def foo(): return 42"
  Module(body=[FunctionDef(name='foo', args=arguments(args=[], vararg=None, kwarg=None, defaults=[]), body=[Return(value=Num(n=42))], decorator_list=[])])


  def foo():
      return 42


Modification of an AST
----------------------

The AST returned by ``ast.parse()`` can be modified, thus here we have is another way to


Let's write a class that capitalize all the constant strings of a Python program by using ``ast.NodeTransformer``::

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

save it as `capitalize.py <exo4/capitalize.py>`_ and run::

  $> python capitalize.py
  ---origin source---

  def foo():
      print "hello", "world"

  foo()

  ---modified source---


  def foo():
      print 'Hello', 'World'
  foo()
  ---run the new source---
  Hello World


The 2nd Aspect Weaver
---------------------

Let's write an other aspect weaver. It's interesting to log down the start and
end of an invocation of functions a function.

Let's firstly consider the simplest case:
we log down the functions invoked as single expressions::

  import sys
  import ast
  from unparse import Unparser
  import os

  class InvocationLogger(ast.NodeTransformer):

      def visit_Expr(self, node):
          if isinstance(node.value, ast.Call):
              before_node, after_node = self.make_around_nodes(node.value.func.id, node.lineno, node.col_offset)
              return [before_node, node, after_node]
          return node

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
          InvocationLogger().visit(tree)
          output_file = "logged_" + filename
          with open(output_file, 'wb') as f_out:
              Unparser(tree, f_out)
              print "write generated code into {}".format(output_file)
          eval(compile(tree, "", "exec"))


Save the code in `ast_aspect.py <exo4/ast_aspect.py>`_,
and let's write a test file `test.py <exo4/test.py>`_::

  def hello(arg):
      inner_fn('Good')
      print 'hello', arg

  def inner_fn(arg):
      print "inner function:", arg

  if __name__ == "__main__":
      hello("World!")


Run this test::

  $> python ast_aspect.py test.py
  write generated code into logged_test.py
  --before call:hello
  --before call:inner_fn
  inner function: Good
  --after call:inner_fn
  hello World!
  --after call:hello

And let's checkout the generated code::

  $> cat logged_test.py


  def hello(arg):
      print '--before call:inner_fn'
      inner_fn('Good')
      print '--after call:inner_fn'
      print 'hello', arg

  def inner_fn(arg):
      print 'inner function:', arg
  if (__name__ == '__main__'):
      print '--before call:hello'
      hello('World!')
      print '--after call:hello'


Note that it's hard to log down all the function calls with this approch, we will need to
consider all invocation cases to inject the code.
For example, an assign operation may include a function call::

  result = foo()


the exepected output should then be::

    print '--before call:foo'
    result = foo('World!')
    print '--after call:foo'

another even trickier case::

  result = foo() + foo()

What would the expected output code be? We may need to consider all invocation cases,
and produce different code for different case. Yes, we are writing a source to source compiler!

Another approch to solve this problem is to change the function definition.
In the body of a function definition, we insert a print expression at the beginning,
then a print expression before the function ends, and before all the return statements.
Here is an example code `ast_aspect2.py <exo4/ast_aspect2.py>`_, in which we only add print message
a message at the begining and at the end of the function body.

Implementing aspect weaver using ``ast`` allows us have more control over the source code,
however, it's also more difficult to code.

=============
Python Weaver
=============


Tricks of Aspect Oriented Programming
=====================================

PATH
----

``wc`` allows us to count the number of lines of a file.

let's try to create a text file named ``test_file.txt`` with the content::

  this
  is
  a
  plain
  text
  file
  :D

Then run::

  $> wc -l test_file.txt
  7 test_file.txt

This means the ``test_file.txt`` has 7 lines.
Let's checkout the absolote path of this command::

  $> which wc
  /usr/bin/wc

Let's create our own script named ``wc`` and put this command inside.
Meanwhile, say hello before executing the command::

  #!/bin/sh
  echo "hello, here is the thing that you should know about:"
  exec /usr/bin/wc $*

Run it::

  ./wc -l test_file.txt
  hello, things that you should know about:
  7 test_file.txt

**Something fun**

Let's create another script named ``hello_wc``, in which we modify our PATH
before running the command ``wc``::

  #!/bin/sh
  export PATH=$PWD:$PATH
  wc $*

Run it::

  $> ./hello_wc -l test_file.txt
  hello, things that you should know about:
  7 test_file.txt

After modifying the ``$PATH`` variable, it's our
own ``wc`` script that has been called, since the shell found the ``wc``
program in current directory first.
We have sucessfully injected code before executing the real ``wc`` program :)


LD_PRELOAD
----------

In this section, we are going to show how to replace a C standard function
with our own implementation of that function by using ``LD_PRELOAD`` variable.

Let's create a hello world ``hello.c``::

  #include <stdio.h>

  int main() {
    printf("Hello world !\n");
    return 0;
  }

Compile and run it::

  $> gcc hello.c -o hello && ./hello
  Hello world !

Let's use ``nm`` to inspect the standard function used by the ``hello`` program::

  $> nm hello
  0000000000601040 B __bss_start
  0000000000601040 b completed.6973
  0000000000601030 D __data_start
  0000000000601030 W data_start
  0000000000400470 t deregister_tm_clones
  00000000004004e0 t __do_global_dtors_aux
  0000000000600e18 t __do_global_dtors_aux_fini_array_entry
  0000000000601038 D __dso_handle
  0000000000600e28 d _DYNAMIC
  0000000000601040 D _edata
  0000000000601048 B _end
  00000000004005c4 T _fini
  0000000000400500 t frame_dummy
  0000000000600e10 t __frame_dummy_init_array_entry
  0000000000400708 r __FRAME_END__
  0000000000601000 d _GLOBAL_OFFSET_TABLE_
                   w __gmon_start__
  00000000004003e0 T _init
  0000000000600e18 t __init_array_end
  0000000000600e10 t __init_array_start
  00000000004005d0 R _IO_stdin_used
                   w _ITM_deregisterTMCloneTable
                   w _ITM_registerTMCloneTable
  0000000000600e20 d __JCR_END__
  0000000000600e20 d __JCR_LIST__
                   w _Jv_RegisterClasses
  00000000004005c0 T __libc_csu_fini
  0000000000400550 T __libc_csu_init
                   U __libc_start_main@@GLIBC_2.2.5
  000000000040052d T main
                   U puts@@GLIBC_2.2.5
  00000000004004a0 t register_tm_clones
  0000000000400440 T _start
  0000000000601040 D __TMC_END__


One of the undefined function we called (with flag ``U``) is ``puts@@GLIBC_2.2.5``,
which is called by ``printf`` function.
This function will be loaded dynamically when running the program.

Let's create a file named ``myiolib.c`` in which we define our own ``puts`` function::

  #include <unistd.h>
  #include <string.h>

  int puts(const char *str) {
    write(1, "I would like to say:\n", 22);
    write(1, str, strlen(str));
    write(1, "\n", 1);
    return 0;
  }


and compile it::

  $> gcc -shared -fPIC myiolib.c -o myiolib.so

``LD_PRELOAD`` is a list of additional, user-specified, ELF shared objects to be loaded before all others.
So let's add ``myiolib.so`` into this list::

  $> export LD_PRELOAD=$PWD/myiolib.so:$LD_PRELOAD

Now, if we run the ``hello`` program again, we will get more stuff printed than we expected::

  $> ./hello
  I would like to say:
  Hello world !

Great, again, we have sucessfully injected code into a C program.

Python decorator
----------------

A Python decorator is a function or class that takes a function as a parameter
and returns another function. Let's use this to do some fun experiments.

**decorator function**

Let's print the trace stack before calling a function::

  import traceback

  def tbdecorator(fn):
      def wrapper():
          traceback.print_stack()
          return fn()
      return wrapper

  @tbdecorator
  def foo():
      print("hello foo")

  def toto():
      foo()

  if __name__ == "__main__":
      toto()

Save the above script into ``decorator.py`` and run it::

  $> python decorator.py
    File "decorator.py", line 17, in <module>
      toto()
    File "decorator.py", line 14, in toto
      foo()
    File "decorator.py", line 5, in wrapper
      traceback.print_stack()
  hello foo


**class decorator**

Let's do the same thing but using class decorator. Moreover, we print the stack only
if the stack contains a function called ``bar()``::

  import traceback

  class mydecorator(object):
      def __init__(self, arg):
          self.arg = arg

      def __call__(self, fn):
          def wrapper(arg):
              print(self.arg)
              for s in traceback.extract_stack():
                  if (s[3] == 'bar()' ):
                      print("function bar() found!")
                      traceback.print_stack()
              return fn(arg)
          return wrapper

  @mydecorator("arg of decorator")
  def foo(arg):
      print("foo:" + arg)

  def bar():
      print("bar() is called")
      foo("hihi")

  if __name__ == "__main__":
      bar()

Save it as ``decorator_class.py``, and run it::

  $> python decorator_class.py
  bar() is called
  arg of decorator
  function bar() found!
    File "decorator_class.py", line 30, in <module>
      bar()
    File "decorator_class.py", line 26, in bar
      foo("hihi")
    File "decorator_class.py", line 14, in wrapper
      traceback.print_stack()
  foo:hihi


Some highlights about the decorators:

1. To apply an action to a function, it's sufficient to declare a declarator
before the function's signature.

2. By using class decorator, we can pass additional arguments.

3. By parsing and analysing the trace stack inside a decorator, we can
apply different actions to different functions.

Therefore, Python's decorator can be a tool for aspect oriented programming.


Python's Introspection
======================

dir() & globals()
-----------------

``globals()`` returns the dictionary containing the current scope's global variables.
``dirs()`` returns the names in the current scope, if called without an argument.

If we define funcitons directely on a Python interpreter (for example ``ipython``),
we can find that the function names can be found in the global variables.

Therefore we can also redefine a global variable to modify its behavior::

  $> ipython
  In [1]: def foo(arg):
     ...:     print("Hello " + arg)
     ...:

  In [2]: foo("man")
  Hello man

  In [3]: globals()["foo"] = lambda x: x ** 2

  In [4]: foo(12)
  Out[4]: 144


isinstance() & type
-------------------

``isinstance()`` and ``type()`` allow us to determine the type of a variable.
Let's use them to filter the global functions::

  $> ipython
  In [1]: def foo(arg):
     ...:     print("Hello " + arg)
     ...:

  In [2]: import types

  In [3]: [fn for fn in globals().values() if isinstance(fn, types.FunctionType)]
  Out[3]: [<function __main__.foo>]

  In [4]: [fn for fn in globals().values() if type(fn) is types.FunctionType]
  Out[4]: [<function __main__.foo>]


Passing parameters
------------------

**Wrapper**

By using unnamed parameters and dictionary parameters,
we can define a function wrapper. Instead of calling a function
directely, we can pass it to the wrapper so that the wrapper can
do some extra work before running the function::

  def wrap(f, *args, **kwargs):
    print("wrap is called with arguments:")
    print ("*args = " + str(args))
    print ("**kwargs = " + str(kwargs))
    f(*args, **kwargs)

  def foo(*args, **kwargs):
      print("foo is called with arguments:")
      print ("*args = " + str(args))
      print ("**kwargs = " + str(kwargs))

  if __name__ == "__main__":
      wrap(foo, 1, 2, ["a", "b"], hi="hihi")


save the code as ``wrapper.py`` and run it::

  $> python wrapper.py
  wrap is called with arguments:
  *args = (1, 2, ['a', 'b'])
  **kwargs = {'hi': 'hihi'}
  foo is called with arguments:
  *args = (1, 2, ['a', 'b'])
  **kwargs = {'hi': 'hihi'}


**Generic decorator**

Based on the wrapper function previously defined, let's
create a generic decorator that can accept all parameters of
a function and pass it to that function::

  def generic_decorator(fn):
      def wrap(*args, **kwargs):
          print("wrap is called with arguments:")
          print("*args = " + str(args))
          print("**kwargs = " + str(kwargs))
          return fn(*args, **kwargs)
      return wrap

  @generic_decorator
  def foo(x, y, *args, **kwargs):
      print("foo is called with arguments:")
      print('x = {}, y = {}'.format(x, y))
      print("*args = " + str(args))
      print("**kwargs = " + str(kwargs))

  if __name__ == "__main__":
      foo(1, 2, ["a", "b"], hi="hihi")


save it as `generic_decorator.pyt` and run::

  $> python generic_decorator.py
  wrap is called with arguments:
  *args = (1, 2, ['a', 'b'])
  **kwargs = {'hi': 'hihi'}
  foo is called with arguments:
  x = 1, y = 2
  *args = (['a', 'b'],)
  **kwargs = {'hi': 'hihi'}



Redefine functions on the fly
-----------------------------

The ``generic_decorator`` returns a new function when it is called.
We can keep this function an use it later. In this case, it's not
used as decorator, so lets rename it as ``fwrapp`` and test it::

  def fwrap(fn):
      def wrap(*args, **kwargs):
          print("wrap is called with arguments:")
          print ("*args = " + str(args))
          print ("**kwargs = " + str(kwargs))
          fn(*args, **kwargs)
      return wrap

  def foo(x, y, *args, **kwargs):
      print("foo is called with arguments:")
      print('x = {}, y = {}'.format(x, y))
      print("*args = " + str(args))
      print("**kwargs = " + str(kwargs))


  if __name__ == "__main__":
      wrapped_foo = fwrap(foo)
      wrapped_foo(1, 2)


save it as ``fwrap.py`` and run::

  $> python fwrap.py
  wrap is called with arguments:
  *args = (1, 2)
  **kwargs = {}
  foo is called with arguments:
  x = 1, y = 2
  *args = ()
  **kwargs = {}

The 1st Aspect Weaver
=====================

Let's write a first aspect weaver using all the knowledge we have have previously talked about.

Before beginning, let's do a little exercise to clarify some basic concepts.

* join point: a point during the execution of a program, such as an execution of a method.
* advice: action taken by an aspect at a particular join point.

Firstely, let's start with some basic wrappers::

  def before_call(join_point, advice):
      def wrap(*args, **kwargs):
          advice(*args, **kwargs)
          return join_point(*args, **kwargs)
      return wrap

  def after_call(join_point, advice):
      def wrap(*args, **kwargs):
          join_point(*args, **kwargs)
          return advice(*args, **kwargs)
      return wrap


  def around_call(join_point, advice_before, advice_after):
      def wrap(*args, **kwargs):
          advice_before(*args, **kwargs)
          join_point(*args, **kwargs)
          return advice_after(*args, **kwargs)
      return wrap

These wrappers allows us to call some advice functions before, after, or around a join point function.
Run the script ``aspect.py``::

  $> python aspect::
  advice:this is before_call test
  foo:this is before_call test
  ========
  foo:this is after_call test
  advice:this is after_call test
  ========
  advice_before:this is around_call test
  foo:this is around_call test
  advice_after:this is around_call test

Now let's do something fun: write a function
``weave(regex, advice_before=None, advice_after=None)``.

This function will check for each loaded modules or top level functions,
if they satisfy the regular expression, then let's apply the advices to that function::

  def weave(regex, advice_before=None, advice_after=None):
      """
      Apply the advices to the functions that matches the regular expression.

      The regex contains 1 or 2 part.
      * If it cannot be saparated by '\.', then it's considered as a top level
      function pattern.
      * Otherwise, the first part is considered as an already loaded top level module,
      and the second part is a function pattern in that module.

      For example, 'foo*' means all top level functions with a name started with 'foo',
      're.*\.c.*' mease all functions started with 'c' of all modules started with 're'.
      """
      if advice_before is None and advice_after is None:
          return  # nothing to do

      splits = regex.split('\.')
      if len(splits) == 1:
          fn_re = splits[0]
          fn_pattern = re.compile(fn_re)
          for name, fn in globals().items():
              if not fn_pattern.match(name) or not isinstance(fn, types.FunctionType):
                  continue
              # weave it !
              if advice_before and advice_after:
                  globals()[name] = around_call(fn, advice_before, advice_after)
              elif advice_before:
                  globals()[name] = before_call(fn, advice_before)
              elif advice_after:
                  globals()[name] = after_call(fn, advice_before)


      elif len(splits) == 2:
          module_re = splits[0]
          fn_re = splits[1]
          fn_pattern = re.compile(fn_re)
          module_pattern = re.compile(module_re)
          # lookup the modules already loaded
          for name, module in globals().items():
              if not module_pattern.match(name) or not isinstance(module, types.ModuleType):
                  continue
              for name in dir(module):
                  fn = getattr(module, name)
                  if not isinstance(fn, types.FunctionType) or not fn_pattern.match(name):
                      continue
                  #weave it!
                  if advice_before and advice_after:
                      setattr(module, name, around_call(fn, advice_before, advice_after))
                  elif advice_before:
                      setattr(module, name, before_call(fn, advice_before))
                  elif advice_after:
                      setattr(module, name, after_call(fn, advice_after))


Let's run the script ``aspect_2.py``::

  === test 1 ===
  -- before calling compile
  matched!
  === test 2 ===
  -- before calling compile
  -- before calling foo_bar
  foo_bar:hi, I'm weaved, amn't I ?
  -- after calling foo_bar
  bar:I'm not weaved:)


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


save it as ``dynamic_compile.py`` and run it::

  $> python dynamic_compile.py "def foo(): return 42"
  Module(body=[FunctionDef(name='foo', args=arguments(args=[], vararg=None, kwarg=None, defaults=[]), body=[Return(value=Num(n=42))], decorator_list=[])])


  def foo():
      return 42


Modification of an AST
----------------------

The AST returned by ``ast.parse()`` can be modified, thus here we have is another way to
inject (or even modify) the origin code.

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

save it as ``capitalize.py`` and run::

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


Save the code in ``ast_aspect.py``, before testing it,
let's write a test file ``test.py``::

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

another case that is even trickier::

  result = foo() + foo()

What would the expected output code be?

To avoid this, we can directely change the function definition.
In the body of a function definition, we insert a print expression at the beginning,
then a print expression before the function ends, and before all the return statements.
Here is an example code ``ast_aspect2.py``

Implementing aspect weaver using ``ast`` allows us have more control over the source code,
however, it's also more difficult to code.

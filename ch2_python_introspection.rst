Python's Introspection
======================

dir() & globals()
-----------------

``globals()`` returns the dictionary containing the current scope's global variables.
``dir()`` returns the names in the current scope, if called without an argument.

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


save the code as `wrapper.py <exo2_python_introspection/wrapper.py>`_ and run it::

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


save it as `generic_decorator.py <exo2_python_introspection/generic_decorator.py>`_ and run::

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
          return fn(*args, **kwargs)
      return wrap

  def foo(x, y, *args, **kwargs):
      print("foo is called with arguments:")
      print('x = {}, y = {}'.format(x, y))
      print("*args = " + str(args))
      print("**kwargs = " + str(kwargs))


  if __name__ == "__main__":
      wrapped_foo = fwrap(foo)
      wrapped_foo(1, 2)


save it as `fwrap.py <exo2_python_introspection/fwrap.py>`_ and run::

  $> python fwrap.py
  wrap is called with arguments:
  *args = (1, 2)
  **kwargs = {}
  foo is called with arguments:
  x = 1, y = 2
  *args = ()
  **kwargs = {}


`Next section: The 1st Aspect Weaver <ch3_first_aspect_weaver.rst>`_

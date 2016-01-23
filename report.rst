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
Let's see where this is absolote path of this command::

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

 TODO

Python Decorator
----------------



Python's Introspection
======================

dir() & globals()
-----------------


isinstance() & type
-------------------


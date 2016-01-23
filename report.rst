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

Python Decorator
----------------



Python's Introspection
======================

dir() & globals()
-----------------


isinstance() & type
-------------------


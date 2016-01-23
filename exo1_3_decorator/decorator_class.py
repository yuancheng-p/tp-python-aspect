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

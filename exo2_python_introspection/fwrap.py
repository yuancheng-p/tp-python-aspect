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

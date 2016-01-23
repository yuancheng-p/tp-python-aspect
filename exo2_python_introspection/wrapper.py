def wrap(f, *args, **kwargs):
    print("wrap is called with arguments:")
    print ("*args = " + str(args))
    print ("**kwargs = " + str(kwargs))
    f(*args, **kwargs)

def foo(*args, **kwargs):
    print("foo is called with arguments:")
    print ("*args = " + str(args))
    print ("*kwargs = " + str(kwargs))

if __name__ == "__main__":
    wrap(foo, 1, 2, ["a", "b"], hi="hihi")

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

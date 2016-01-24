def hello(arg):
    inner_fn('Good')
    print 'hello', arg

def inner_fn(arg):
    print "inner function:", arg

if __name__ == "__main__":
    hello("World!")


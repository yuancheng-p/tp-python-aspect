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


def foo(arg):
    print("foo:" + arg)

def advice(arg):
    print("advice:" + arg)

def advice_before(arg):
    print("advice_before:" + arg)

def advice_after(arg):
    print("advice_after:" + arg)

if __name__ == "__main__":
    before_foo = before_call(foo, advice)
    before_foo("this is before_call test")

    print ("=" * 8)
    after_foo = after_call(foo, advice)
    after_foo("this is after_call test")

    print ("=" * 8)
    around_foo = around_call(foo, advice_before, advice_after)
    around_foo("this is around_call test")


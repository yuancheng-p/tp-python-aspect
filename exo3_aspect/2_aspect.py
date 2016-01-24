import re
import types

def before_call(join_point, advice):
    def wrap(*args, **kwargs):
        advice(join_point.__name__, *args, **kwargs)
        return join_point(*args, **kwargs)
    return wrap


def after_call(join_point, advice):
    def wrap(*args, **kwargs):
        join_point(*args, **kwargs)
        return advice(join_point.__name__, *args, **kwargs)
    return wrap


def around_call(join_point, advice_before, advice_after):
    def wrap(*args, **kwargs):
        advice_before(join_point.__name__, *args, **kwargs)
        join_point(*args, **kwargs)
        return advice_after(join_point.__name__, *args, **kwargs)
    return wrap

"""
regex represent a top level module pattern,
followed by a function pattern. ex: r're.*\.m.*'
"""
def weave(regex, advice_before=None, advice_after=None):
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


def foo_bar(arg):
    print("foo_bar:" + arg)


def bar(arg):
    print ("bar:" + arg)


def before_advice(fn_name, *args, **kwargs):
    print("-- before calling " +  fn_name)


def after_advice(fn_name, *args, **kwargs):
    print("-- after calling " +  fn_name)


if __name__ == "__main__":
    print('=== test 1 ===')
    weave(r're.*\.c.*', advice_before=before_advice)
    p = re.compile('[0-9]+')
    if p.match('123'):
        print 'matched!'

    print('=== test 2 ===')
    weave(r'foo.*', advice_before=before_advice, advice_after=after_advice)

    foo_bar("hi, I'm weaved, amn't I ?")
    bar("I'm not weaved:)")

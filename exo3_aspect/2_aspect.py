import re
import types

"""
regex represent a top level module pattern,
followed by a function pattern. ex: r're.*\.m.*'
"""
def weave_before(regex, advice):

    splits = regex.split('\.')
    if len(splits) == 1:
        fn_re = splits[0]
        fn_pattern = re.compile(fn_re)
        for name, fn in globals().items():
            if fn_pattern.match(name) and isinstance(fn, types.FunctionType):
                globals()[name] = before_call(fn, advice)  # weave it !

    elif len(splits) == 2:
        module_re = splits[0]
        fn_re = splits[1]
        fn_pattern = re.compile(fn_re)
        module_pattern = re.compile(module_re)
        # lookup the modules already loaded
        for name, module in globals().items():
            if module_pattern.match(name) and isinstance(module, types.ModuleType):
                for name in dir(module):
                    fn = getattr(module, name)
                    if isinstance(fn, types.FunctionType) and fn_pattern.match(name):
                        setattr(module, name, before_call(fn, advice))  # weave it !


def before_call(join_point, advice):
    def wrap(*args, **kwargs):
        advice(join_point.__name__, *args, **kwargs)
        return join_point(*args, **kwargs)
    return wrap


def foo_bar(arg):
    print("foo_bar:" + arg)


def bar(arg):
    print ("bar:" + arg)


def my_advice(fn_name, *args, **kwargs):
    print("calling " +  fn_name)



if __name__ == "__main__":
    print('--- test 1 ---')
    weave_before(r're.*\.c.*', my_advice)
    p = re.compile('[0-9]+')
    if p.match('123'):
        print 'matched!'

    print('--- test 2 ---')
    weave_before(r'foo.*', my_advice)
    foo_bar("hi, I'm weaved, amn't I ?")
    bar("I'm not weaved:)")

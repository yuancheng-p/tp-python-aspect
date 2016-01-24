The 1st Aspect Weaver
=====================

Let's write a first aspect weaver using all the knowledge we have have previously talked about.

Before beginning, let's do a little exercise to clarify some basic concepts.

* join point: a point during the execution of a program, such as an execution of a method.
* advice: action taken by an aspect at a particular join point.

Firstely, let's start with some basic wrappers::

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

These wrappers allows us to call some advice functions before, after, or around a join point function.
Run the script `aspect.py <exo3_aspect/aspect.py>`_::

  $> python aspect::
  advice:this is before_call test
  foo:this is before_call test
  ========
  foo:this is after_call test
  advice:this is after_call test
  ========
  advice_before:this is around_call test
  foo:this is around_call test
  advice_after:this is around_call test

Now let's do something fun: write a function
``weave(regex, advice_before=None, advice_after=None)``.

This function will check for each loaded modules or top level functions,
if they satisfy the regular expression, then let's apply the advices to that function::

  def weave(regex, advice_before=None, advice_after=None):
      """
      Apply the advices to the functions that matches the regular expression.

      The regex contains 1 or 2 part.
      * If it cannot be saparated by '\.', then it's considered as a top level
      function pattern.
      * Otherwise, the first part is considered as an already loaded top level module,
      and the second part is a function pattern in that module.

      For example, 'foo*' means all top level functions with a name started with 'foo',
      're.*\.c.*' mease all functions started with 'c' of all modules started with 're'.
      """
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


Let's run the script `aspect_2.py <exo3_aspect/aspect_2.py>`_ ::

  === test 1 ===
  -- before calling compile
  matched!
  === test 2 ===
  -- before calling compile
  -- before calling foo_bar
  foo_bar:hi, I'm weaved, amn't I ?
  -- after calling foo_bar
  bar:I'm not weaved:)


`Next section: Aspect Weaver with ast module <ch4_ast_aspect_weaver.rst>`_

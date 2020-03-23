#region Errors
class KwargParseError(Exception): pass
class ArgumentError(KwargParseError): pass
class ArgumentTypeError(ArgumentError): pass
class ArgumentRequiredError(ArgumentError): pass
#endregion

_type_class = type

#region Namespace class
class _AttributeHolder(object):
    """Abstract base class that provides __repr__.
    The __repr__ method returns a string in the format::
        ClassName(attr=name, attr=name, ...)
    The attributes are determined either by a class-level attribute,
    '_kwarg_names', or by inspecting the instance __dict__.
    """

    def __repr__(self):
        type_name = type(self).__name__
        arg_strings = []
        star_args = {}
        for arg in self._get_args():
            arg_strings.append(repr(arg))
        for name, value in self._get_kwargs():
            if name.isidentifier():
                arg_strings.append('%s=%r' % (name, value))
            else:
                star_args[name] = value
        if star_args:
            arg_strings.append('**%s' % repr(star_args))
        return '%s(%s)' % (type_name, ', '.join(arg_strings))

    def _get_kwargs(self):
        return sorted(self.__dict__.items())

    def _get_args(self):
        return []

class Namespace(_AttributeHolder):
    """Simple object for storing attributes.
    Implements equality by attribute names and values, and provides a simple
    string representation.
    NOTE:: Copied from argparse
    """

    def __init__(self, **kwargs):
        for name in kwargs:
            setattr(self, name, kwargs[name])

    def __eq__(self, other):
        if not isinstance(other, Namespace):
            return NotImplemented
        return vars(self) == vars(other)

    def __contains__(self, key):
        return key in self.__dict__
#endregion

#region Types
def AnyType(obj):
    return obj
#endregion

def _run_action(action, kwargs):
    if hasattr(action, '__call__'):
        return action(kwargs)
    elif hasattr(action, 'parse'):
        return action.parse(kwargs)
    elif hasattr(action, '_parse_as_arg'):
        return action._parse_as_arg(kwargs)

class _NULL_RESULT: pass

#region Actions
class Action:
    def __init__(self, names, required=True, default=None, type=AnyType):
        self.names = names
        self.required = required
        self.default = default
        self.type = type
    def parse(self): pass
    def _parse_as_arg(self): pass

class _Argument(Action):
    def __call__(self, kwargs):
        for name in self.names:
            if name in kwargs:
                try: result = self.type(kwargs[name])
                except ArgumentError as e:
                    raise e from None
                else: break
        else:
            if self.required:
                raise ArgumentRequiredError('argument %s required to be passed' % self.names[0]) from None
            else: result = self.default
        return result
#endregion

class KeywordArgumentParser:
    def __init__(self):
        self._args = []
        # self._error_exception = None
    @classmethod
    def _init_as_subparser(cls, names, required=True, default=None):
        self = cls()
        Action.__init__(self, names, required, default)
        return self
    def parse_kwargs(self, kwargs) -> Namespace:
        result = {}
        for arg in self._args:
            _run_action(arg, kwargs)
        return Namespace(**result)
    # def _raise_none(self): pass
    # def _raise(self, message): pass
    # def set_error_exception(self, klass, message_format=''):
    #     self._error_exception = (klass, message_format)
    def add_argument(self, *names, dest=None, required=True, default=None, type=AnyType, action=_Argument):
        self._args.append(action(names, required, default, type))
    def add_subparser(self, *names, required=True, default=None):
        subparser = self.__class__._init_as_subparser(names, required, default)
        self._args.append(subparser)
        return subparser
    def _parse_as_arg(self, kwargs):
        kwargs = _Argument.__call__(self, kwargs)
        return self.parse_kwargs(kwargs)
from argparse import Namespace

#region Errors
class KwargParseError(Exception): pass
class ArgumentError(KwargParseError): pass
class ArgumentTypeError(ArgumentError): pass
class ArgumentRequiredError(ArgumentError): pass
#endregion

_type_class = type

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
    def __init__(self, names, dest=None, required=None, default=None, type=AnyType):
        if dest is None: dest = names[0]
        if required is None:
            if default is None:
                required = True
            else: required = False
        self.names = names
        self.dest = dest
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
                except Exception as e:
                    raise e from None
                else: break
        else:
            if self.required:
                raise ArgumentRequiredError('argument %s required to be passed' % self.names[0]) from None
            else:
                name = None
                result = self.default
        return name, result
#endregion

class KeywordArgumentParser:
    def __init__(self):
        self._args = []
        # self._error_exception = None
    @classmethod
    def _init_as_subparser(cls, names, dest=None, required=None, default=None):
        self = cls()
        Action.__init__(self, names, dest, required, default)
        return self
    def parse_kwargs(self, kwargs) -> Namespace:
        result = {}
        all_names = set()
        used = set()
        for arg in self._args:
            all_names.update(arg.names)
            name, result[arg.dest] = _run_action(arg, kwargs)
            if name is not None: used.add(name)
        extras = used - all_names
        if extras:
            raise IndexError('extra arguments passed: %s' % ', '.join(str(extra) for extra in extras)) from None
        return Namespace(**result)
    # def _raise_none(self): pass
    # def _raise(self, message): pass
    # def set_error_exception(self, klass, message_format=''):
    #     self._error_exception = (klass, message_format)
    def add_argument(self, *names, dest=None, required=None, default=None, type=AnyType, action=_Argument):
        self._args.append(action(names, dest, required, default, type))
    def add_subparser(self, *names, dest=None, required=None, default=None):
        subparser = self.__class__._init_as_subparser(names, dest, required, default)
        self._args.append(subparser)
        return subparser
    def _parse_as_arg(self, kwargs):
        name, kwargs = _Argument.__call__(self, kwargs)
        return name, self.parse_kwargs(kwargs)

#region Metadata
__version__ = '1.0.0'
__author__ = 'Gaming32'
__all__ = ['KwargParseError', 'ArgumentError', 'ArgumentTypeError', 'ArgumentRequiredError',
           'AnyType',
           'Action',
           'KeywordArgumentParser',
           'Namespace']
#endregion
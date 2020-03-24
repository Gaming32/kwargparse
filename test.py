import kwargparse

_kwarg_parser = kwargparse.KeywordArgumentParser()
def _init_kwarg_parser():
    _kwarg_parser.add_argument('hello')
    subp = _kwarg_parser.add_subparser('sub', default={'world': 20})
    subp.add_argument('world', default=20)
    def ftemp(v):
        if v is not None:
            raise TypeError(v)
    _kwarg_parser.add_argument('errors', type=ftemp, required=False)

def main(**kwargs):
    result = _kwarg_parser.parse_kwargs(kwargs)
    print(result)
    print(result.sub.world)

_init_kwarg_parser()

if __name__ == '__main__':
    main(
        hello = 1,
        sub = dict(
            world = 2,
        ),
        errors = 5,
    )
import kwargparse

_kwarg_parser = kwargparse.KeywordArgumentParser()
def _init_kwarg_parser():
    _kwarg_parser.add_argument('hello')

def main(**kwargs):
    result = _kwarg_parser.parse_kwargs(kwargs)
    print(result)

_init_kwarg_parser()

if __name__ == '__main__':
    main(
        hello = 1
    )
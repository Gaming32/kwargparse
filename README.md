![PyPI](https://img.shields.io/pypi/v/kwargparse)
![PyPI - Format](https://img.shields.io/pypi/format/kwargparse)
![License](https://img.shields.io/github/license/gaming32/kwargparse)
![PyPI - Downloads](https://img.shields.io/pypi/dm/kwargparse)
![GitHub last commit](https://img.shields.io/github/last-commit/gaming32/kwargparse)
![GitHub wheel size in bytes](https://img.shields.io/github/size/gaming32/kwargparse/dist/kwargparse-1.0.0-py3-none-any.whl?label=wheel%20size)
![GitHub top language](https://img.shields.io/github/languages/top/gaming32/kwargparse)

# Using this tool
This tool's format is very similar to that of the `argparse` module. Example setup:
``` python
import kwargparse

_kwarg_parser = kwargparse.KeywordArgumentParser()
def _init_kwarg_parser():
    _kwarg_parser.add_argument('hello')
    subp = _kwarg_parser.add_subparser('sub', default={'world': 20})
    subp.add_argument('world', default=20)

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
    )
```
# Installing
To install simply use:
``` shell
$ pip3 install kwargparse
```
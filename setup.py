import setuptools

with open('README.md', 'r') as fp:
    long_description = fp.read()

setuptools.setup(
    name = 'kwargparse',
    version = '1.0.0',
    author = 'Gaming32',
    author_email = 'gaming32i64@gmail.com',
    license = 'License :: OSI Approved :: MIT License',
    description = "Parser that parses Python's kwargs similar to the way done by setuptools, while exporting an interface like argparse",
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    setup_requires = [
        'argparse',
    ],
    py_modules = [
        'kwargparse',
    ]
)
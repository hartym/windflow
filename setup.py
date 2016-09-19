# This file is autogenerated by edgy.project code generator.
# All changes will be overwritten.

from setuptools import setup, find_packages

tolines = lambda c: list(filter(None, map(lambda s: s.strip(), c.split('\n'))))

def read(filename, flt=None):
    with open(filename) as f:
        content = f.read().strip()
        return flt(content) if callable(flt) else content

try:
    version = read('version.txt')
except:
    version = 'dev'

setup(
    name = 'windflow',
    description = ('Windflow is a toolkit for creating web applications faster with tornado and '
 'asyncio.'),
    license = 'Apache 2.0',
    install_requires = ['Jinja2 ==2.8',
 'SQLAlchemy ==1.1.0b3',
 'psycopg2 ==2.6.2',
 'python-dotenv ==0.6.0',
 'tornado ==4.4.1',
 'uvloop ==0.5.3',
 'simplejson'],
    version = version,
    long_description = read('README.rst'),
    classifiers = read('classifiers.txt', tolines),
    packages = find_packages(exclude=['ez_setup', 'example', 'test']),
    include_package_data = True,
    extras_require = {'dev': ['coverage >=4.0,<4.2',
         'honcho >=0.7,<0.8',
         'mock >=2.0,<2.1',
         'nose >=1.3,<1.4',
         'pylint >=1.6,<1.7',
         'pytest >=2.9,<2.10',
         'pytest-cov >=2.3,<2.4',
         'sphinx',
         'sphinx_rtd_theme']},
    url = 'https://github.com/hartym/windflow',
    download_url = 'https://github.com/hartym/windflow/archive/{version}.tar.gz'.format(version=version),
)

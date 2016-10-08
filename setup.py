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
    description = ('Windflow is a rapid web application development toolkit using tornado, '
 'asyncio and sqlalchemy.'),
    license = 'Apache 2.0',
    install_requires = ['Jinja2 ==2.8',
 'SQLAlchemy ==1.1.1',
 'alembic ==0.8.8',
 'honcho ==0.7.1',
 'psycopg2 ==2.6.2',
 'python-dotenv ==0.6.0',
 'simplejson ==3.8.2',
 'tornado ==4.4.2'],
    version = version,
    long_description = read('README.rst'),
    classifiers = read('classifiers.txt', tolines),
    packages = find_packages(exclude=['ez_setup', 'example', 'test']),
    include_package_data = True,
    extras_require = {'alembic': ['alembic ==0.8.8'],
 'dev': ['coverage >=4.2,<4.3',
         'honcho >=0.7,<0.8',
         'mock >=2.0,<2.1',
         'nose >=1.3,<1.4',
         'pylint >=1.6,<1.7',
         'pytest >=3.0,<3.1',
         'pytest-cov >=2.3,<2.4',
         'sphinx >=1.4,<1.5',
         'sphinx_rtd_theme'],
 'uvloop': ['uvloop ==0.5.4']},
    url = 'https://github.com/hartym/windflow',
    download_url = 'https://github.com/hartym/windflow/archive/{version}.tar.gz'.format(version=version),
)

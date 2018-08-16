from __future__ import print_function
from setuptools import setup, find_packages
import sys
import crawel_utils

if sys.version_info < (3, 4):
    sys.exit('Python 3.4 or greater is required')

setup(
    name="simplecat",
    version=crawel_utils.version,
    author="Acke",
    author_email="vimer757216574@gmail.com",
    description="A python3 library for download Movie comment from Maoyan",
    long_description=open("README.md").read(),
    license="Apache",
    url='https://github.com/VIMerhan/MaoyanCrawel',
    platforms=['all'],
    packages=find_packages(where='.',exclude=(),include=('*',)),
    install_requires=[
        'beautifulsoup4>=4.6.0'
        'builtwith>=1.3.3'
        'certifi>=2016.2.28'
        'requests>=2.14.2'
        'simplejson=>=3.11.1'
        'six=>=1.11.0'
        'threadpool=>=1.3.2'
        'lxml=>=4.2.4'
        'pymongo>=3.4.0'
        'tqdm>=4.15.0'
    ],
    zip_safe=False,

)

import os
import codecs
import re
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

requires = [
        'requests==2.18.1',
        'jsonschema==2.6.0',
        'requests-toolbelt==0.8.0'
]

tests_require = []

setup(
    name='neuroseed',
    version=find_version('neuroseed/__init__.py'),
    description='Neuroseed platform REST API wrapper',
    author='Ihor Omelchenko',
    author_email='counter3d@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    packages=find_packages(exclude=['examples', 'docs', 'tests']),
    install_requires=requires,
    extras_require={
        'testing': tests_require,
    },
    test_suite='tests'
)

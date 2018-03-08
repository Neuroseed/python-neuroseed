from setuptools import setup, find_packages
import neuroseed

setup(
    name='neuroseed',
    version=neuroseed.__version__,
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
    install_requires=['requests']
)


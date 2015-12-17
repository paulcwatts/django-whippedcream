#!/usr/bin/env python
import os
import codecs
from setuptools import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

if os.path.exists('README.rst'):
    long_description = codecs.open('README.rst', 'r', 'utf-8').read()
else:
    long_description = 'See https://github.com/paulcwatts/django-whippedcream'

setup(
    name='django-whippedcream',
    version='0.2.2',
    author='Paul Watts',
    author_email='paulcwatts@gmail.com',
    description='Utilities that make tastypie taste better.',
    license='BSD',
    url='https://github.com/paulcwatts/django-whippedcream',
    include_package_data=True,
    packages=[
        'whippedcream',
        'whippedcream.runtests',
        'whippedcream.tests'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    long_description=long_description
)

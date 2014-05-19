#!/usr/bin/env python
# encoding: utf-8
import os
import sys

from setuptools import setup, find_packages


version = __import__('achilles').get_version()

def dump(filename):
    return open(os.path.join(os.path.dirname(__file__), filename))

extra = {}

# Use 2to3 for Python 3 support
if sys.version_info >= (3, 0):
    extra.update(
        use_2to3=True,
    )

setup(
    name='django-achilles',
    version=version,
    url='http://github.com/exekias/django-achilles/',
    author='Carlos Pérez-Aradros Herce',
    author_email='exekias@gmail.com',
    description='Django AJAX Framework',
    long_description=dump('README.rst').read(),
    packages=find_packages(exclude=['example', '*.tests', '*.tests.*']),
    include_package_data=True,
    install_requires=[r.strip() for r in dump('requirements.txt')],
    tests_require=[r.strip() for r in dump('requirements-dev.txt')],
    zip_safe=False,
    license='Apache License (2.0)',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    **extra
)

# encoding: utf-8
from setuptools import setup, find_packages


version = __import__('achilles').get_version()

setup(
    name='django-achilles',
    version=version,
    url='http://github.com/exekias/django-achilles/',
    author='Carlos Pérez-Aradros Herce',
    author_email='cperez@zentyal.com',
    description='Django AJAX Framework',
    packages=find_packages(exclude=['demo', '*.tests']),
    install_requires=[line for line in open('requirements.txt')],
)

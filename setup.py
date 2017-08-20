#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-camera-imagefield',
    version='0.1.2',
    description="A Django widget for using a device's camera to get an image to upload",
    author='Alexander Dutton',
    author_email='code@alexdutton.co.uk',
    url='https://github.com/alexsdutton/django-camera-imagefield',
    packages=find_packages(),
    install_requires=['django', 'python-datauri'],
    include_package_data=True,
)

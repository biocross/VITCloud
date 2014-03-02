#!/usr/bin/env python

from setuptools import setup

setup(
    name='VITCloudDev',
    version='1.0',
    description='OpenShift App',
    author='Siddharth Gupta',
    author_email='example@example.com',
    url='http://www.python.org/sigs/distutils-sig/',
    install_requires=['Django<=1.4', 'oauth2>=1.5.167', 'python_openid>=2.2', 'selenium>=2.29.0', 'mock==1.0.1', 'django-social-auth'],
)

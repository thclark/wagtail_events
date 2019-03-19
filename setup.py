#!/usr/bin/env python
from __future__ import unicode_literals

from wagtail_events import __version__
from setuptools import setup, find_packages

setup(
    name='omni_wagtail_events',
    version=__version__,
    description='Event features for Wagtail',
    author='Omni Digital',
    author_email='dev@omni-digital.co.uk',
    url='https://github.com/omni-digital/omni-wagtail-events',
    download_url='https://github.com/omni-digital/omni-wagtail-events/tarball/1.1.1',
    packages=find_packages(),
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    include_package_data=True,
    install_requires=[
        'wagtail>=1.8.0',
        'isoweek==1.1.0',
        'python-dateutil==2.6.0'
    ],
    keywords=['wagtail', 'django', 'events']
)

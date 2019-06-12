#!/usr/bin/env python

# Note:
#
#   This medium article descripbes the travis / releases integration steps:
#       https://medium.com/@mikkokotila/deploying-python-packages-to-pypi-with-travis-works-9a6597781556
#
#   The Hitchiker's guide to python provides an excellent, standard, method for creating python packages:
#       http://docs.python-guide.org/en/latest/writing/structure/
#
#   To deploy on PYPI follow the instructions at the bottom of:
#       https://packaging.python.org/tutorials/distributing-packages/#uploading-your-project-to-pypi

from setuptools import setup, find_packages

with open('README.md') as f:
    readme_text = f.read()

setup(
    name='wagtail_events',
    version='0.2.7',
    description='Event pages for Wagtail',
    long_description=readme_text,
    long_description_content_type="text/markdown",
    author='thclark',
    author_email='withheld.find@me.at.github.com',
    url='https://github.com/thclark/wagtail_events',
    packages=find_packages(exclude=('tests', 'docs')),
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Operating System :: OS Independent"
    ],
    include_package_data=True,
    install_requires=[
        'wagtail>=2.3',
        'isoweek==1.3.3',
        'python-dateutil==2.8.0'
    ],
    keywords=['wagtail', 'django', 'events']
)

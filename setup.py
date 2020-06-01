
#!/usr/bin/env python
# -*- coding: utf-8 -*

from __future__ import absolute_import

import os
from codecs import open

from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

with open('README.md', 'r', encoding='utf-8') as rm_file:
    readme = rm_file.read()

with open('HISTORY.md', 'r', encoding='utf-8') as hist_file:
    history = hist_file.read()

setup(
    name='django_rename_app',
    version='0.1.0',
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    zip_safe=False,
    description=(
        'A Django Management Command to rename existing Django Applications.'
    ),
    author='O\'Dwyer Software',
    author_email='hello@odwyer.software',
    url='https://github.com/odwyersoftware/django-rename-app',
    license='Apache 2.0',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    install_requires=install_requires,
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)

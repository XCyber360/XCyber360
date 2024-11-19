# Copyright (C) 2015-2023, Xcyber360 Inc.
# Created by Xcyber360, Inc. <info@xcyber360.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2
from setuptools import setup, find_namespace_packages
import shutil
import glob


setup(
    name='xcyber360-qa-framework',
    version='1.0.0',
    description='Xcyber360 testing utilities to help programmers automate tests',
    url='https://github.com/xcyber360/xcyber360/tree/master/qa/system',
    author='Xcyber360',
    author_email='hello@xcyber360.com',
    license='GPLv2',
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src'),
    zip_safe=False
)

# Clean build files
shutil.rmtree('dist')
shutil.rmtree('build')
shutil.rmtree(glob.glob('src/*.egg-info')[0])

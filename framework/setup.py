#!/usr/bin/env python



from xcyber360 import __version__

from setuptools import setup, find_namespace_packages

setup(name='xcyber360',
      version=__version__,
      description='Xcyber360 control with Python',
      url='https://github.com/xcyber360',
      author='Xcyber360',
      author_email='hello@xcyber360.com',
      license='GPLv2',
      packages=find_namespace_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      package_data={'xcyber360': ['core/xcyber360.json',
                              'core/cluster/cluster.json', 'rbac/default/*.yaml']},
      include_package_data=True,
      install_requires=[],
      zip_safe=False,
      )

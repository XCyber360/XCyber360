#!/usr/bin/env python


from setuptools import setup, find_namespace_packages

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

setup(
    name='api',
    version='5.0.0',
    description="Xcyber360 API",
    author_email="hello@xcyber360.com",
    author="Xcyber360",
    url="https://github.com/xcyber360",
    keywords=["Xcyber360 API"],
    install_requires=[],
    packages=find_namespace_packages(exclude=["*.test", "*.test.*", "test.*", "test"]),
    package_data={'': ['spec/spec.yaml']},
    include_package_data=True,
    zip_safe=False,
    license='GPLv2',
    long_description="""\
    The Xcyber360 API is an open source RESTful API that allows for interaction with the Xcyber360 manager from a web browser, command line tool like cURL or any script or program that can make web requests. The Xcyber360 app relies on this heavily and Xcyber360’s goal is to accommodate complete remote management of the Xcyber360 infrastructure via the Xcyber360 app. Use the API to easily perform everyday actions like adding an agent, restarting the manager(s) or agent(s) or looking up syscheck details.
    """
)

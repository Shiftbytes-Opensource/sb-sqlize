from setuptools import find_packages, setup

setup(
    name='sqlize',
    packages=find_packages(include= ["sqlize"]),
    version='0.0.1',
    description='JSON to SQL converter. The idea is cereate a library / logic that lets you create a DBMS table from simple JSON text. This lib is not limited to that, it can also get data as JSON and convet it as SQL text for storing.',
    author='Sreenath',
    license='GNU GPLv3',
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests'
)

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pythymiodw',
    version='2.4.1',
    description='Python library for Thymio used in Digital World class',
    long_description=long_description,
    url='https://github.com/kurniawano/pythymiodw',
    author='Oka Kurniawan',
    author_email='kurniawano@ieee.org',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Education',
        ],
    keywords='robot library education',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['libdw', 'pygame', 'requests', 'Pyro4', 'cryptography'],
    package_data={
        'pythymiodw': ['thymiohandlers.aesl','images/iodisplay.png'],
        'pythymiodw.pg':['images/thymio1.png', 'images/thymio2.png', 'images/thymio3.png', 'images/thymio4.png', 'images/thymio5.png'],
        },
    )

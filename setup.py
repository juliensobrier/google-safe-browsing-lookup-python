import os
import sys

from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requirements = []

setup(
    name='Google Safe Browsing v2 Lookup',
    version='0.1.0',
    py_modules=['safebrowsinglookup'],
    description='Client to interact with the Google Safe Browsing v2 Lookup API',
    long_description=read('README'),
    url='https://github.com/juliensobrier/google-safe-browsing-lookup-python',
    license='Apache',
    author='Julien Sobrier',
    author_email='julien@sobrier.net',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    packages=find_packages(),
    namespace_packages=["safebrowsinglookup"],
    install_requires=requirements,
)
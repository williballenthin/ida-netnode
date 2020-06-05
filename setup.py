#!/usr/bin/env python

from setuptools import setup

setup(name='ida-netnode',
      version="2.0",
      description="Humane API for storing and accessing persistent data in IDA Pro databases",
      author='Willi Ballenthin',
      author_email='william.ballenthin@fireeye.com',
      url='https://github.com/williballenthin/ida-netnode',
      license='Apache License (2.0)',
      packages=['netnode'],
      install_requires=[
          "six",
      ],
      classifiers=["Programming Language :: Python",
                   "Programming Language :: Python :: 2",
                   "Programming Language :: Python :: 3",
                   "Operating System :: OS Independent",
                   "License :: OSI Approved :: Apache Software License"
                  ],
     )

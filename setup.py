#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='diligence',
      version='0.0.1',
      description='Lets you ',
      author='Frank Stratton',
      license='MIT',
      author_email='frank@runscope.com',
      url='',
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      platforms='any',
      install_requires=[
          'requests',
      ],
      entry_points={
          'console_scripts': [
              'diligence = diligence:main',
          ]
      },
)

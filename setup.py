from setuptools import setup, find_packages

VERSION = '0.1'

setup(name='369-lt',
      version=VERSION,
      packages=find_packages('src'),
      install_requires=[
          'distribute',
      ],
      url='',
      license='GPL',
      description='a369.',
      long_description=open('README.rst').read(),
      )

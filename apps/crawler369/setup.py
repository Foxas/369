from setuptools import setup, find_packages

VERSION = '0.1'

setup(name='crawler369',
      version=VERSION,
      packages=find_packages(),
      install_requires=[
          'distribute',
      ],
      url='',
      license='GPL',
      description='crawler369.',
      long_description=open('README.rst').read(),
      )

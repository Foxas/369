from setuptools import setup, find_packages

version = '0.1.1'

setup(name="threesixnine",
      version=version,
      description="Social monitoring service 369.lt",
      long_description=open("README.rst").read() + "\n" +
                       open("HISTORY.rst").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Team 369',
      author_email='',
      url='http://www.369.lt',
      license='GPL',
      packages=find_packages('src'),
      package_dir = {'':'src'},
      include_package_data=True,
      package_data={'web369':['*.html', '*.po', '*.css', '*.js'], },
      zip_safe=False,
      install_requires=[
          'setuptools',
          'django',
      ],
      entry_points="""
      [console_scripts]
      threesixnine-django = web369.scripts.manage:main
      """,
      )

from setuptools import setup, find_packages

version = '0.2.0'

setup(name='qthmi.ads',
      version=version,
      description='',
      long_description="""\
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['qthmi'],
      include_package_data=True,
      test_suite='nose.collector',
      test_requires=['Nose'],  
      zip_safe=False,
      install_requires=[
          'setuptools',
	  'matplotlib',
	  'qthmi.main',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )

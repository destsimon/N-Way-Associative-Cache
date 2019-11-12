from setuptools import setup, find_packages

setup(name='n-way-associative-cache',
      version='0.2',
      author='Alex de St. Simon',
      author_email='alex@destsimon.com',
      description='NWayAssociativeCache',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False)
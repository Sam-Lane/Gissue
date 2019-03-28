from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='gissue',
      version='0.3',
      description='Command line tool for managing GitHub project issues.',
      url='http://github.com/sam-lane/gissue',
      author='Sam Lane',
      author_email='gissue@samlane.io',
      license='MIT',
      long_description=long_description,
      packages=['gissue'],
      install_requires=[
            'Requests==2.21.0',
            'Colr==0.8.3',
      ],
      zip_safe=False)
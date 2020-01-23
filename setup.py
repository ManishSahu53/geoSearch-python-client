import re
from io import open

from setuptools import find_packages, setup

# Get the long description from the relevant file
with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

with open('geoSearch/VERSION') as version_file:
    __version__ = version_file.read().strip()

setup(name='geoSearch',
      version=__version__,
      description="This repo is python client for geoSearch system of APIs to search and process satellite dataset",
      long_description=long_description,
      classifiers=[
          'License :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: Scientific/Engineering :: GIS',
          'Topic :: Utilities',
      ],
      keywords='GIS, Cloud, GDAL',
      author="Manish Sahu",
      author_email='manish.sahu.civ13@iitbhu.ac.in',
      url='https://github.com/ManishSahu53/geoSearch-python-client.git',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=open('requirements.txt').read().splitlines(),
      extras_require={
          'dev': [
              'requests',
              'tqdm'
          ],
      },
      #   entry_points="""
      #   [console_scripts]
      #   sentinelsat=sentinelsat.scripts.cli:cli
      #   """
      )

# MD to  RST
# pandoc --from=markdown --to=rst --output=README.rst README.md

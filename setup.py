from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize

with open("README.md", "r") as fh:
    long_description = fh.read()

#for the time being only with cython:
USE_CYTHON = True


extensions = [Extension(
                         name='cykhash.khashsets',
                         sources = ["src/cykhash/khashsets.pyx"],
                        ),
              Extension(
                         name='cykhash.khashmaps',
                         sources = ["src/cykhash/khashmaps.pyx"],
                        ),
              Extension(
                         name='cykhash.unique',
                         sources = ["src/cykhash/unique.pyx"],
                        ),
             ]


if USE_CYTHON:
    extensions = cythonize(extensions, language_level=3)

kwargs = {
      'name':'cykhash',
      'version':'1.0.1',
      'description':'cython wrapper for khash-sets/maps, efficient implementation of `isin` and `unique`',
      'author':'Egor Dranischnikow',
      'long_description':long_description,
      'long_description_content_type':"text/markdown",
      'url':'https://github.com/realead/cykhash',
      'packages':find_packages(where='src'),
      'package_dir':{"": "src"},
      'license': 'MIT',
      'classifiers': [
            "Programming Language :: Python :: 3",
       ],
      'ext_modules':  extensions,

       #ensure pxd-files:
      'package_data' : { 'cykhash': ['*.pxd','*.pxi','*/*/*.pxi']},
      'include_package_data' : True,
      'zip_safe' : False  #needed because setuptools are used
}


setup(**kwargs)


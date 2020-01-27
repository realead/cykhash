from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize



#for the time being only with cython:
USE_CYTHON = True



extensions = Extension(
            name='cykhash.khashsets',
            sources = ["cykhash/khashsets.pyx"],
    )

if USE_CYTHON:
    extensions = cythonize(extensions, language_level=3)

kwargs = {
      'name':'cykhash',
      'version':'0.3.0',
      'description':'Cython wrapper for khash-table',
      'author':'Egor Dranischnikow',
      'url':'https://github.com/realead/cykhash',
      'packages':find_packages(),
      'license': 'MIT',
      'ext_modules':  extensions,

       #ensure pxd-files:
      'package_data' : { 'cykhash': ['*.pxd','*.pxi']},
      'include_package_data' : True,
      'zip_safe' : False  #needed because setuptools are used
}


setup(**kwargs)


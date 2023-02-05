from setuptools import setup, find_namespace_packages, Extension

from Cython import Tempita
from Cython.Build import cythonize

import os

with open("README.md", "r") as fh:
    long_description = fh.read()


#for the time being only with cython:
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
              Extension(
                         name='cykhash.utils',
                         sources = ["src/cykhash/utils.pyx"],
                        ),
             ]


template_files = ["src/cykhash/maps/map_impl.pxi.in",
                  "src/cykhash/maps/map_init.pxi.in",
                  "src/cykhash/maps/map_header.pxi.in",
                  "src/cykhash/sets/set_impl.pxi.in",
                  "src/cykhash/sets/set_header.pxi.in",
                  "src/cykhash/sets/set_init.pxi.in",
                  "src/cykhash/unique/unique_impl.pxi.in",
]

def render_templates(pxifiles):
        for pxifile in pxifiles:
            # build pxifiles first, template extension must be *.in
            outfile = pxifile[:-3]

            if (
                os.path.exists(outfile)
                and os.stat(pxifile).st_mtime < os.stat(outfile).st_mtime
            ):
                # if .pxi.in is not updated, no need to output .pxi
                continue

            with open(pxifile) as f:
                tmpl = f.read()
            pyxcontent = Tempita.sub(tmpl)

            with open(outfile, "w") as f:
                f.write(pyxcontent)


def my_cythonize(extensions):
    # prepare templates:
    render_templates(template_files)
    #cythonize extensions:
    return cythonize(extensions, language_level=3)
 

kwargs = {
      'name':'cykhash',
      'version':'2.0.1',
      'description':'cython wrapper for khash-sets/maps, efficient implementation of isin and unique',
      'author':'Egor Dranischnikow',
      'long_description':long_description,
      'long_description_content_type':"text/markdown",
      'url':'https://github.com/realead/cykhash',
      'packages':find_namespace_packages(where='src'),
      'package_dir':{"": "src"},
      'license': 'MIT',
      'classifiers': [
            "Programming Language :: Python :: 3",
       ],
      'ext_modules':  my_cythonize(extensions),

       #ensure pxd-files:
      'package_data' : { 'cykhash': ['*.pxd','*.pxi','*/*/*.pxi','*/*.pxi.in']},
      'include_package_data' : True,
      'zip_safe' : False,  #needed because setuptools are used
}


setup(**kwargs)


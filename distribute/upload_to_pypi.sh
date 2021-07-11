
DISTRO="cykhash-2.0.0.tar.gz"

cd ..

# clean up
rm -rf dist
pip uninstall cykhash


# create sdist
python setup.py sdist


# test:
cd dist
pip install "$DISTRO"
cd ../tests
sh run_unit_tests.sh 
sh run_doctests.sh

#clean up
pip uninstall cykhash


# test distro
cd ..
twine check dist/"$DISTRO"

# test upload to test
twine upload --repository-url https://test.pypi.org/legacy/ dist/"$DISTRO"

cd tests 
sh test_install.sh from-test-pypi
cd ..


# upload to pypi
twine upload dist/"$DISTRO"

cd tests 
sh test_install.sh from-pypi




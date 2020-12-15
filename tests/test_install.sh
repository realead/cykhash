set -e

ENV_DIR="../p3"
virtualenv -p python3 "$ENV_DIR"
echo "Testing python3"


#activate environment
. "$ENV_DIR/bin/activate"

python -c "import setuptools; print('setuptools version:', setuptools.__version__)"

# test installation in clean environment
if [ "$1" = "from-github" ]; then
    pip install https://github.com/realead/cykhash/zipball/master
elif [ "$1" = "from-test-pypi" ]; then
    pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple cykhash
elif [ "$1" = "from-pypi" ]; then
    pip install cykhash
else
      (cd .. && python -m pip install .)
#     (cd .. && python setup.py build install)
fi;

# needed for testing:
pip install numpy
pip install cython
pip install pytest
pip install https://github.com/realead/uttemplate/zipball/master

pip freeze

sh run_unit_tests.sh



#clean or keep the environment
if [ "$2" = "keep" ]; then
   echo "keeping enviroment $ENV_DIR"
else
   rm -r "$ENV_DIR"
fi;


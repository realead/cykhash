set -e

ENV_DIR="../p3"
virtualenv -p python3 "$ENV_DIR"
echo "Testing python3"


#activate environment
. "$ENV_DIR/bin/activate"

#prepare:
pip install cython
pip install numpy
pip install https://github.com/realead/uttemplate/zipball/master

if [ "$1" = "from-github" ]; then
    pip install https://github.com/realead/cykhash/zipball/master
elif [ "$1" = "from-test-pypi" ]; then
    pip install -i https://test.pypi.org/simple/ cykhash
elif [ "$1" = "from-pypi" ]; then
    pip install cykhash
else
    (cd .. && python setup.py install)
fi;

pip freeze

sh run_unit_tests.sh



#clean or keep the environment
if [ "$2" = "keep" ]; then
   echo "keeping enviroment $ENV_DIR"
else
   rm -r "$ENV_DIR"
fi;


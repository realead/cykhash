
export ROOTPATH="$PWD/.."

export PYTHONPATH="${PYTHONPATH}:$ROOTPATH"

if [ "$1" = "rebuild" ]; then
    (cd $ROOTPATH && python setup.py build_ext --inplace --force)
fi;

sh run_unit_tests.sh


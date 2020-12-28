echo "\n\nTesting md-files....":
(cd .. && pytest --ignore=tests --doctest-glob=*.md -vv  --doctest-continue-on-failure)

echo "\n\nTesting pyx and pxi from installation..."
python run_installed_doctests.py 

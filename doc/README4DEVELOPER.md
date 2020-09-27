# cykhash for developers (i.e. future me)

## Dependencies:

Essential:

  * Cython>=0.28 because verbatim C-code feature is used
  * build tool chain (for example gcc on Linux)

Additional dependencies for testing:

  * `sh`
  * `virtualenv`
  * `uttemplate`>=0.2.0 (https://github.com/realead/uttemplate)
  * `numpy`, `pandas`, `perfplot` for performance tests
  * `asv` for asv_bench testing (performance tests)



## Testing:

For testing of the local version in an virtual environment run:

    sh test_install.sh 

in the `tests` subfolder.

For testing of the version from github run:

    sh test_install.sh from-github

For keeping the the virtual enviroment after the tests:

    sh test_install.sh local keep

To install and running tests in currently active environment:

    sh test_in_active_env.sh

For comparing performance of the HEAD with upstream/master:

    sh run_asv_bench.sh

you might want to reduce the number of tests - see examples in `run_asv_bench.sh`


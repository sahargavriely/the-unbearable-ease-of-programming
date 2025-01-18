#!/bin/bash


function main {
    source venv/bin/activate
    cd docs/
    make html SPHINXOPTS="-W"
    export TEST_RESULT=$?
    cd ..
    deactivate
    exit ${TEST_RESULT}
}


main "$@"

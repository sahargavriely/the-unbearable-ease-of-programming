#!/bin/bash


function main {
    source .env/bin/activate
    cd docs/
    make html SPHINXOPTS="-W"
    export TEST_REULST=$?
    cd ..
    deactivate
    exit ${TEST_REULST}
}


main "$@"

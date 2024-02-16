#!/bin/bash


function main {
    source venv/bin/activate
    pytest --cov-report=html --cov-report=xml --cov-report=term --cov=brain_computer_interface tests/
    export TEST_REULST=$?
    deactivate
    exit ${TEST_REULST}
}


main "$@"

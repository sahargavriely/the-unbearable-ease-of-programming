#!/bin/bash


function main {
    source venv/bin/activate
    pytest --cov-branch --cov-report=html --cov-report=xml --cov-report=term --cov=brain_computer_interface tests/
    export TEST_RESULT=$?
    deactivate
    exit ${TEST_RESULT}
}


main "$@"

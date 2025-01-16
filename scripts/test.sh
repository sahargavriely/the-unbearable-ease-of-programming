#!/bin/bash


function main {
    venv/bin/python -m pytest --cov-branch --cov-report=html --cov-report=xml --cov-report=term --cov=brain_computer_interface tests/
    export TEST_REULST=$?
    exit ${TEST_REULST}
}


main "$@"

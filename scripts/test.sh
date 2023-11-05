#!/bin/bash


function main {
    source .env/bin/activate
    pytest --cov-report=html --cov-report=xml --cov-report=term --cov=brain_computer_interface tests/
    export TEST_STATUS=$?
    rm -f tests-status.RUNNING
    if [[ ${TEST_STATUS} -eq 0 ]]; then
        touch tests-status.SUCCESS
    else
        touch tests-status.FAILED
    fi
    deactivate
    exit ${TEST_STATUS}
}


main "$@"

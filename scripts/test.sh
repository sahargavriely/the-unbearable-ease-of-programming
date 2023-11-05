#!/bin/bash


function main {
    source .env/bin/activate
    python -m pytest --cov-report html --cov brain_computer_interface tests/
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

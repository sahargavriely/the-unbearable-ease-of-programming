#!/bin/bash


function main {
    source .env/bin/activate
    python -m pytest --cov-report html --cov brain_computer_interface tests/
    deactivate
}


main "$@"

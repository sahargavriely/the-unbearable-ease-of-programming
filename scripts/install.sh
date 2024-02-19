#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function main {
    pip install --upgrade pip
    pip install virtualenv
    python -m virtualenv venv --prompt "brain-computer-interface"
    find venv -name site-packages -exec bash -c 'echo "../../../../" > {}/self.pth' \;
    venv/bin/pip install -U pip
    venv/bin/pip install -r requirements.txt
}


main "$@"

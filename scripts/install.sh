#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function main {
    pip install --upgrade pip
    pip install virtualenv
    python -m virtualenv .env --prompt "brain-computer-interface"
    find .env -name site-packages -exec bash -c 'echo "../../../../" > {}/self.pth' \;
    .env/bin/pip install -U pip
    .env/bin/pip install -r requirements.txt
}


main "$@"

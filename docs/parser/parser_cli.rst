CLI Reference
=============


The ``brain-computer-interface.parser`` package provides a command line interface:

.. code:: bash

    $ python -m brain_computer_interface.parser --help
    Usage: brain_computer_interface.parser [OPTIONS] COMMAND [ARGS]...

    Options:
    --version        Show the version and exit.
    -q, --quiet
    -t, --traceback
    --help           Show this message and exit.

    Commands:
    error
    parse
    run-parser


The top-level options include:

- ``-q``, ``--quiet``

    This option suppresses the output.

- ``-t``, ``--traceback``

    This option shows the full traceback when an exception is raised (by
    default, only the error message is printed, and the program exits with a
    non-zero code).


The ``parse`` Command
---------------------

Receives parser name (you can explore more about parsers at :ref:`parsers file <target to parsers>`) and path to file a file with a raw snapshot data; and the parsed data.

.. code:: bash

    $ python -m brain_computer_interface.parser parse --help
    Usage: brain_computer_interface.parser parse [OPTIONS] NAME DATA_PATH

    Options:
    -s, --shared-dir PATH  [default: shared]
    --help                 Show this message and exit.


The ``run-parser`` command
~~~~~~~~~~~~~~~~~~~~~~~~~~

Receives parser name (you can explore more about parsers at :ref:`parsers file <target to parsers>`) and running a service which listens to the parser subscribe handle.

.. code:: bash

    $ python -m brain_computer_interface.parser run-parser --help
    Usage: brain_computer_interface.parser run-parser [OPTIONS] NAME

    Options:
    -s, --shared-dir PATH         [default: shared]
    -d, --distribute-scheme TEXT  [default: rabbitmq://localhost:5672/]
    -g, --group
    --help                        Show this message and exit.


The ``error`` Command
---------------------

Raises an exception and prints it to the screen.

.. code:: bash

    $ python -m brain_computer_interface.parser error --help
    Usage: brain_computer_interface.parser error [OPTIONS]

    Options:
    --help  Show this message and exit.


All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

To showcase these options, consider `error` command, which raises an exception:

.. code:: bash

    $ python -m brain_computer_interface.parser error
    ERROR: something went terribly wrong :[
    $ python -m brain_computer_interface.parser -q error  # suppress output
    $ python -m brain_computer_interface.parser -t error  # show full traceback
    ERROR: something went terribly wrong :[
    Traceback (most recent call last):
        ...
    RuntimeError: something went terrible wrong :[


Do note that each command's options should be passed to *that* command, for example the ``-q`` and ``-t`` options should be passed to ``brain_computer_interface.parser`` and not to ``parse`` and ``run-parser``.

.. code:: bash

    $ python -m brain_computer_interface.parser parse -q  # this doesn't work
    ERROR: no such option: -q
    $ python -m brain_computer_interface.parser -q parse  # this does work

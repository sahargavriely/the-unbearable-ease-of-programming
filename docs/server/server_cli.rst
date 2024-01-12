CLI Reference
=============


The ``brain-computer-interface.server`` package provides a command line interface:

.. code:: bash

    $ python -m brain_computer_interface.server --help
    Usage: brain_computer_interface.server [OPTIONS] COMMAND [ARGS]...

    Options:
    --version        Show the version and exit.
    -q, --quiet
    -t, --traceback
    --help           Show this message and exit.

    Commands:
    error
    run-server


The top-level options include:

- ``-q``, ``--quiet``

    This option suppresses the output.

- ``-t``, ``--traceback``

    This option shows the full traceback when an exception is raised (by
    default, only the error message is printed, and the program exits with a
    non-zero code).


.. _target to run-server:

The ``run-server`` Command
--------------------------

Runs the server on ``host:port`` which listens to minds and forwarding them to the driver corresponding to the ``--publish-scheme`` argument.

.. code:: bash

    $ python -m brain_computer_interface.server run-server --help
    Usage: brain_computer_interface.server run-server [OPTIONS]

    Options:
    -d, --distribute-scheme TEXT  [default: rabbitmq://localhost:5672/]
    -h, --host TEXT               [default: 0.0.0.0]
    -p, --port INTEGER            [default: 5000]
    -s, --shared-dir PATH         [default: shared]
    --help                        Show this message and exit.


The ``error`` Command
---------------------

Raises an exception and prints it to the screen.

.. code:: bash

    $ python -m brain_computer_interface.server error --help
    Usage: brain_computer_interface.server error [OPTIONS]

    Options:
    --help  Show this message and exit.


All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

To showcase these options, consider `error` command, which raises an exception:

.. code:: bash

    $ python -m brain_computer_interface.server error
    ERROR: something went terribly wrong :[
    $ python -m brain_computer_interface.server -q error  # suppress output
    $ python -m brain_computer_interface.server -t error  # show full traceback
    ERROR: something went terribly wrong :[
    Traceback (most recent call last):
        ...
    RuntimeError: something went terrible wrong :[


Do note that each command's options should be passed to *that* command, for example the ``-q`` and ``-t`` options should be passed to ``brain_computer_interface.server`` and not to ``run-server``.

.. code:: bash

    $ python -m brain_computer_interface.server run-server -q  # this doesn't work
    ERROR: no such option: -q
    $ python -m brain_computer_interface.server -q run-server  # this does work

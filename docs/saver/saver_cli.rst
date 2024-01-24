CLI Reference
=============


The ``brain-computer-interface.saver`` package provides a command line interface:

.. code:: bash

    $ python -m brain_computer_interface.saver --help
    Usage: brain_computer_interface.saver [OPTIONS] COMMAND [ARGS]...

    Options:
    --version        Show the version and exit.
    -q, --quiet
    -t, --traceback
    --help           Show this message and exit.

    Commands:
    error
    run-saver


The top-level options include:

- ``-q``, ``--quiet``

    This option suppresses the output.

- ``-t``, ``--traceback``

    This option shows the full traceback when an exception is raised (by
    default, only the error message is printed, and the program exits with a
    non-zero code).


Top Level Command ``save``
--------------------------

Top level command which supports ``snapshot`` and ``user`` from file.

.. code:: bash

    $ python -m brain_computer_interface.saver save --help
    Usage: brain_computer_interface.saver save [OPTIONS] COMMAND [ARGS]...

    Options:
    --help  Show this message and exit.

    Commands:
    snapshot
    user


Sub Command ``snapshot``
------------------------

Reads a given path content as json format and saves it as a snapshot to the database.

.. code:: bash

    $ python -m brain_computer_interface.saver save snapshot --help
    Usage: brain_computer_interface.saver save snapshot [OPTIONS] USER_ID DATETIME TOPIC PATH

    Options:
    -d, --database TEXT            [default: postgresql://postgres:password@127.0.0.1:5432/mind]
    --help  Show this message and exit.


Sub Command ``user``
--------------------

Reads a given path content as json format and saves it as a user to the database.

.. code:: bash

    $ python -m brain_computer_interface.saver save user --help
    Usage: brain_computer_interface.saver save user [OPTIONS] USER_ID PATH

    Options:
    -d, --database TEXT            [default: postgresql://postgres:password@127.0.0.1:5432/mind]
    --help  Show this message and exit.


.. _target to run-saver:

The ``run-saver`` Command
--------------------------

Runs the saver which listen to ``parsed`` data and user data and saves them to the database.

.. code:: bash

    $ python -m brain_computer_interface.saver run-saver --help
    Usage: brain_computer_interface.saver run-saver [OPTIONS]

    Options:
    -d, --database TEXT            [default: postgresql://postgres:password@127.0.0.1:5432/mind]
    -ds, --distribute-scheme TEXT  [default: rabbitmq://localhost:5672/]
    --help                         Show this message and exit.


The ``error`` Command
---------------------

Raises an exception and prints it to the screen.

.. code:: bash

    $ python -m brain_computer_interface.saver error --help
    Usage: brain_computer_interface.saver error [OPTIONS]

    Options:
    --help  Show this message and exit.


All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

To showcase these options, consider `error` command, which raises an exception:

.. code:: bash

    $ python -m brain_computer_interface.saver error
    ERROR: something went terribly wrong :[
    $ python -m brain_computer_interface.saver -q error  # suppress output
    $ python -m brain_computer_interface.saver -t error  # show full traceback
    ERROR: something went terribly wrong :[
    Traceback (most recent call last):
        ...
    RuntimeError: something went terrible wrong :[


Do note that each command's options should be passed to *that* command, for example the ``-q`` and ``-t`` options should be passed to ``brain_computer_interface.saver`` and not to ``run-saver``.

.. code:: bash

    $ python -m brain_computer_interface.saver run-saver -q  # this doesn't work
    ERROR: no such option: -q
    $ python -m brain_computer_interface.saver -q run-saver  # this does work

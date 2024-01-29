CLI Reference
=============


The ``brain-computer-interface.rest`` package provides a command line interface:

.. code:: bash

    $ python -m brain_computer_interface.rest --help
    Usage: brain_computer_interface.rest [OPTIONS] COMMAND [ARGS]...

    Options:
    --version        Show the version and exit.
    -q, --quiet
    -t, --traceback
    --help           Show this message and exit.

    Commands:
    error
    get
    run-rest-server


The top-level options include:

- ``-q``, ``--quiet``

    This option suppresses the output.

- ``-t``, ``--traceback``

    This option shows the full traceback when an exception is raised (by
    default, only the error message is printed, and the program exits with a
    non-zero code).


.. _target to run-rest-server:

The ``run-rest-server`` Command
-------------------------------

Runs the rest on ``host:port`` which listens to minds and forwarding them to the driver corresponding to the ``--publish-scheme`` argument.

.. code:: bash

    $ python -m brain_computer_interface.rest run-rest-server --help
    Usage: brain_computer_interface.rest run-rest-server [OPTIONS]

    Options:
    -h, --host TEXT             [default: 0.0.0.0]
    -p, --port INTEGER          [default: 8000]
    -d, --database-scheme TEXT  [default: postgresql://postgres:password@127.0.0
                                .1:5432/mind]
    --help                      Show this message and exit.


The top level ``get`` Command
-----------------------------

Top level command to stimulate restfull requests.
You may provide host and port to which the requests will be made.

.. code:: bash

    $ python -m brain_computer_interface.rest get --help
    Usage: brain_computer_interface.rest get [OPTIONS] COMMAND [ARGS]...

    Options:
    -h, --host TEXT     [default: 127.0.0.1]
    -p, --port INTEGER  [default: 8000]
    --help              Show this message and exit.

    Commands:
    user
    user-snapshot
    user-snapshot-topic
    user-snapshot-topic-data
    user-snapshots
    users


The ``user`` sub-command
------------------------

Get the user information.

.. code:: bash

    $ python -m brain_computer_interface.rest get user --help
    USAGE: brain_computer_interface.rest get user [OPTIONS] ID


The ``user-snapshot`` sub-command
---------------------------------

Get the user's snapshot information.

.. code:: bash

    $ python -m brain_computer_interface.rest get user-snapshot --help
    USAGE: brain_computer_interface.rest get user-snapshot [OPTIONS] ID DATETIME


The ``user-snapshot-topic`` sub-command
---------------------------------------

Get the user's snapshot's topic information.

.. code:: bash

    $ python -m brain_computer_interface.rest get user-snapshot-topic --help
    USAGE: brain_computer_interface.rest get user-snapshot-topic [OPTIONS] ID DATETIME TOPIC


The ``user-snapshot-topic-data`` sub-command
--------------------------------------------

Get the user's snapshot's topic's data (available for `color_image` and `depth_image`).

.. code:: bash

    $ python -m brain_computer_interface.rest get user-snapshot-topic-data --help
    USAGE: brain_computer_interface.rest get user-snapshot-topic-data [OPTIONS] ID DATETIME TOPIC


The ``user-snapshots`` sub-command
----------------------------------

Get the user's snapshots.

.. code:: bash

    $ python -m brain_computer_interface.rest get user-snapshots --help
    USAGE: brain_computer_interface.rest get user-snapshots [OPTIONS] ID


The ``users`` sub-command
-------------------------

Get all users.

.. code:: bash

    $ python -m brain_computer_interface.rest get users --help
    USAGE: brain_computer_interface.rest get users [OPTIONS]


The ``error`` Command
---------------------

Raises an exception and prints it to the screen.

.. code:: bash

    $ python -m brain_computer_interface.rest error --help
    Usage: brain_computer_interface.rest error [OPTIONS]

    Options:
    --help  Show this message and exit.


All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

To showcase these options, consider `error` command, which raises an exception:

.. code:: bash

    $ python -m brain_computer_interface.rest error
    ERROR: something went terribly wrong :[
    $ python -m brain_computer_interface.rest -q error  # suppress output
    $ python -m brain_computer_interface.rest -t error  # show full traceback
    ERROR: something went terribly wrong :[
    Traceback (most recent call last):
        ...
    RuntimeError: something went terrible wrong :[


Do note that each command's options should be passed to *that* command, for example the ``-q`` and ``-t`` options should be passed to ``brain_computer_interface.rest`` and not to ``run-rest-server``.

.. code:: bash

    $ python -m brain_computer_interface.rest run-rest-server -q  # this doesn't work
    ERROR: no such option: -q
    $ python -m brain_computer_interface.rest -q run-rest-server  # this does work

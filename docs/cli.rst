brain-computer-interface CLI Reference
======================================


The ``brain-computer-interface`` package provides a command line interface:

.. code:: bash

    $ python -m brain_computer_interface [OPTIONS] COMMAND [ARGS]
    ...


The top-level options include:

- ``-q``, ``--quiet``

    This option suppresses the output.

- ``-t``, ``--traceback``

    This option shows the full traceback when an exception is raised (by
    default, only the error message is printed, and the program exits with a
    non-zero code).


To see the version, do the following:

.. code:: bash

    $ python -m brain_computer_interface --version
    brain_computer_interface, version 0.1.0


The ``run-server`` Command
--------------------------

Runs the server which listens to thoughts.

.. code:: bash

    $ python -m brain_computer_interface run-server [OPTIONS]

Options:

- ``-h``, ``--host`` TEXT      [default: 0.0.0.0]
- ``-p``, ``--port`` INTEGER   [default: 5000]
- ``-d``, ``--data_dir`` PATH  [default: data]
- ``-D``, ``--debug``
- ``--help``                   Show similar message and exit.


The ``run-webserver`` Command
-----------------------------

Runs the webserver which makes the users' thoughts accessible.

.. code:: bash

    $ python -m brain_computer_interface run-webserver [OPTIONS]

Options:

- ``-h``, ``--host`` TEXT      [default: 0.0.0.0]
- ``-p``, ``--port`` INTEGER   [default: 8000]
- ``-d``, ``--data_dir`` PATH  [default: data]
- ``-D``, ``--debug``
- ``--help``                   Show similar message and exit.


.. _target to read:

The ``read`` Command
----------------------

Receives :ref:`mind file <target to mind file>` and prints its contents in a humanly fashion.

.. code:: bash

    $ python -m brain_computer_interface read [OPTIONS] PATH

Options:
- ``--help``                  Show similar message and exit.


The ``error`` Command
---------------------

Raises an exception and prints it to the screen.

.. code:: bash

    $ python -m brain_computer_interface error [OPTIONS]

All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

To showcase these options, consider `error` command, which raises an exception:

.. code:: bash

    $ python -m brain_computer_interface error
    ERROR: something went terribly wrong :[
    $ python -m brain_computer_interface -q error  # suppress output
    $ python -m brain_computer_interface -t error  # show full traceback
    ERROR: something went terribly wrong :[
    Traceback (most recent call last):
        ...
    RuntimeError: something went terrible wrong :[


Do note that each command's options should be passed to *that* command, for example the ``-q`` and ``-t`` options should be passed to ``brain_computer_interface`` and not to ``run-server``, ``run_webserver`` and ``upload-thought``.

.. code:: bash

    $ python -m brain_computer_interface run-server -q  # this doesn't work
    ERROR: no such option: -q
    $ python -m brain_computer_interface -q run-server  # this does work

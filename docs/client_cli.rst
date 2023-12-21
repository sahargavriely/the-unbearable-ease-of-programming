CLI Reference
=============


The ``brain-computer-interface.client`` package provides a command line interface:

.. code:: bash

    $ python -m brain_computer_interface.client [OPTIONS] COMMAND [ARGS]
    ...


The top-level options include:

- ``-q``, ``--quiet``

    This option suppresses the output.

- ``-t``, ``--traceback``

    This option shows the full traceback when an exception is raised (by
    default, only the error message is printed, and the program exits with a
    non-zero code).


.. _target to upload-mind:

The ``upload-mind`` command
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Receives :ref:`mind file <target to mind file>`, and uploads it to the server.

.. code:: bash

    $ python -m brain_computer_interface.client upload-mind [OPTIONS] PATH

Options:

- ``-h``, ``--host`` TEXT     [default: 127.0.0.1]
- ``-p``, ``--port`` INTEGER  [default: 5000]
- ``--help``                  Show similar message and exit.


The ``upload-thought`` command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Receives user id and though, and uploads it to the server.

.. code:: bash

    $ python -m brain_computer_interface.client upload-thought [OPTIONS] USER_ID THOUGHT

Options:

- ``-h``, ``--host`` TEXT     [default: 127.0.0.1]
- ``-p``, ``--port`` INTEGER  [default: 5000]
- ``--help``                  Show similar message and exit.


The ``error`` Command
---------------------

Raises an exception and prints it to the screen.

.. code:: bash

    $ python -m brain_computer_interface.client error [OPTIONS]

All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

To showcase these options, consider `error` command, which raises an exception:

.. code:: bash

    $ python -m brain_computer_interface.client error
    ERROR: something went terribly wrong :[
    $ python -m brain_computer_interface.client -q error  # suppress output
    $ python -m brain_computer_interface.client -t error  # show full traceback
    ERROR: something went terribly wrong :[
    Traceback (most recent call last):
        ...
    RuntimeError: something went terrible wrong :[


Do note that each command's options should be passed to *that* command, for example the ``-q`` and ``-t`` options should be passed to ``brain_computer_interface.client`` and not to ``run-server``, ``run_webserver`` and ``upload-thought``.

.. code:: bash

    $ python -m brain_computer_interface.client upload-mind -q  # this doesn't work
    ERROR: no such option: -q
    $ python -m brain_computer_interface.client -q upload-mind  # this does work

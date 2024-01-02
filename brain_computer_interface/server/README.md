# brain-computer-interface.server

Sub-package of brain-computer-interface.
The following package implements a server who knows how to receive minds and thoughts.

For further information take a look at [full documentation](https://the-unbearable-ease-of-programming.readthedocs.io/en/latest/server.html).

## Usage

The `brain_computer_interface.server` packages provides the following function:

- `run_server`

    This function starts the server which receives minds from clients.
    You should provide a ``publish_method`` which the server will forward the data to.
    You may provide an address (host and port) which the server listens to (defaults are set to ``'0.0.0.0'`` and ``5000``, respectfully) a directory in which the server will save the thoughts to (default is set to ``shared/``). 

    ```pycon
    >>> from brain_computer_interface import run_server
    >>> from pathlib import Path
    >>> run_server(print, host='0.0.0.0', port=5000, shared_dir=Path('shared/'))
    {'user': {...}, 'snapshot': {...}}
    ```

## Command Line Interface

The `brain_computer_interface.server` package also provides a command-line interface.
```sh
    $ python -m brain_computer_interface.server [OPTIONS] COMMAND [ARGS]
```

The top-level options include:

- ``-q``, ``--quiet``

    This option suppresses the output.

- ``-t``, ``--traceback``

    This option shows the full traceback when an exception is raised (by
    default, only the error message is printed, and the program exits with a
    non-zero code).

Commands:

- ``run-server``

    Runs the server which listens to thoughts.

    ```sh
    $ python -m brain_computer_interface run-server [OPTIONS]
    ```
    Options:
    - ``-ps``, ``--publish-scheme`` TEXT [default: file:///shared/publish/data.json]
    - ``-h``, ``--host`` TEXT            [default: 0.0.0.0]
    - ``-p``, ``--port`` INTEGER         [default: 5000]
    - ``-s``, ``--shared-dir`` PATH      [default: shared/]
    - ``-D``, ``--debug``
    - ``--help``                         Show similar message and exit.

- `error`

    Raises an exception and prints it to the screen.

    ```sh
    $ python -m brain_computer_interface.server error [OPTIONS]
    ```

    Options:
    - ``--help``                  Show similar message and exit.

All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

To showcase these options, consider `error` command, which raises an exception:

```sh
$ python -m brain_computer_interface.server error
ERROR: something went terribly wrong :[
$ python -m brain_computer_interface.server -q error  # suppress output
$ python -m brain_computer_interface.server -t error  # show full traceback
ERROR: something went terribly wrong :[
Traceback (most recent call last):
    ...
RuntimeError: something went terrible wrong :[
```

Do note that each command's options should be passed to *that* command, for example the `-q` and `-t` options should be passed to `brain_computer_interface.server`, not `run-server`.

```sh
$ python -m brain_computer_interface.server run-server -q  # this doesn't work
ERROR: no such option: -q
$ python -m brain_computer_interface.server -q run-server  # this does work
```

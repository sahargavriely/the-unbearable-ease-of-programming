# brain-computer-interface.rest

Sub-package of brain-computer-interface.
The following package implements a rest who knows how to receive minds and thoughts.

For further information take a look at [full documentation](https://the-unbearable-ease-of-programming.readthedocs.io/en/latest/rest.html).

## Usage

The `brain_computer_interface.rest` packages provides the following function:

- `run_rest_server`

    This function starts the rest server which exposes a restfull api.
    You may provide an address (host and port) which the rest listens to (defaults are set to ``'0.0.0.0'`` and ``5000``, respectfully) and a database scheme (default is set to ``postgresql://postgres:password@127.0.0.1:5432/mind``). 

    ```pycon
    >>> from brain_computer_interface.rest import run_rest_server
    >>> run_rest_server(host='0.0.0.0', port=5000, database_scheme='postgresql://postgres:password@127.0.0.1:5432/mind')
    ...
    ```

## Command Line Interface

The `brain_computer_interface.rest` package also provides a command-line interface.
```sh
    $ python -m brain_computer_interface.rest [OPTIONS] COMMAND [ARGS]
```

The top-level options include:

- ``-q``, ``--quiet``

    This option suppresses the output.

- ``-t``, ``--traceback``

    This option shows the full traceback when an exception is raised (by
    default, only the error message is printed, and the program exits with a
    non-zero code).

Commands:

- ``run-rest-server``

    Runs the rest.

    ```sh
    $ python -m brain_computer_interface.rest run-rest-server [OPTIONS]
    ```
    Options:
    - ``-d``, ``--database-scheme`` TEXT [default: postgresql://postgres:password@127.0.0.1:5432/mind]
    - ``-h``, ``--host`` TEXT            [default: 0.0.0.0]
    - ``-p``, ``--port`` INTEGER         [default: 5000]
    - ``-D``, ``--debug``
    - ``--help``                         Show similar message and exit.

- ``get``

    Top level command to stimulate restfull requests.
    You may provide host and port to which the requests will be made.

    ```sh
    $ brain_computer_interface.rest get [OPTIONS] COMMAND [ARGS]...
    ```
    Options:
    -h, --host TEXT     [default: 127.0.0.1]
    -p, --port INTEGER  [default: 8000]
    --help              Show this message and exit.

    Commands:

    - ``user``

        Get the user information.

        ```sh
        brain_computer_interface.rest get user [OPTIONS] ID
        ```

    - ``user-snapshot``

        Get the user's snapshot information.

        ```sh
        brain_computer_interface.rest get user-snapshot [OPTIONS] ID DATETIME
        ```

    - ``user-snapshot-topic``

        Get the user's snapshot's topic information.

        ```sh
        brain_computer_interface.rest get user-snapshot-topic [OPTIONS] ID DATETIME TOPIC
        ```

    - ``user-snapshot-topic-data``

        Get the user's snapshot's topic's data (available for `color_image` and `depth_image`).

        ```sh
        brain_computer_interface.rest get user-snapshot-topic-data [OPTIONS] ID DATETIME TOPIC
        ```

    - ``user-snapshots``

        Get the user's snapshots.

        ```sh
        brain_computer_interface.rest get user-snapshots [OPTIONS] ID
        ```

    - ``users``

        Get all users.

        ```sh
        brain_computer_interface.rest get users [OPTIONS]
        ```

- `error`

    Raises an exception and prints it to the screen.

    ```sh
    $ python -m brain_computer_interface.rest error [OPTIONS]
    ```

    Options:
    - ``--help``                  Show similar message and exit.

All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

To showcase these options, consider `error` command, which raises an exception:

```sh
$ python -m brain_computer_interface.rest error
ERROR: something went terribly wrong :[
$ python -m brain_computer_interface.rest -q error  # suppress output
$ python -m brain_computer_interface.rest -t error  # show full traceback
ERROR: something went terribly wrong :[
Traceback (most recent call last):
    ...
RuntimeError: something went terrible wrong :[
```

Do note that each command's options should be passed to *that* command, for example the `-q` and `-t` options should be passed to `brain_computer_interface.rest`, not `run-rest-server`.

```sh
$ python -m brain_computer_interface.rest run-rest-server -q  # this doesn't work
ERROR: no such option: -q
$ python -m brain_computer_interface.rest -q run-rest-server  # this does work
```

## Restfull API

Once the rest server is up and running, one execute the following http request at the address the server is on.

- ``/users/<int:id>``

    Get the user information.

- ``/users/<int:id>/snapshots/<int:datetime>``

    Get the user's snapshot information.

- ``/users/<int:id>/snapshots/<int:datetime>/<string:topic>``

    Get the user's snapshot's topic information.

- ``/users/<int:id>/snapshots/<int:datetime>/<string:topic>/data``

    Get the user's snapshot's topic's data (available for `color_image` and `depth_image`).

- ``/users/<int:id>/snapshots``

    Get the user's snapshots.

- ``/users``

    Get all users.

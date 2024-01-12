# brain-computer-interface.client

Sub-package of brain-computer-interface.
The following package allows clients to upload minds (to learn about minds refer to [`message`](/brain_computer_interface/message/README.md)) and thoughts to the server.

For further information take a look at [full documentation](https://the-unbearable-ease-of-programming.readthedocs.io/en/latest/client.html).

## Usage

The `brain_computer_interface.client` packages provides the following functions:

- `upload_mind`

    This function sends a given mind to the server.
    You may also provide an address (host and port) which the function send the information to (defaults are set to ``'127.0.0.1'`` and ``5000``, respectfully). 

    ```pycon
    >>> from brain_computer_interface.client import upload_mind
    >>> upload_mind(mind_path, host='127.0.0.1', port=5000)
    {snapshot.datetime} snapshot uploaded
    {snapshot.datetime} snapshot uploaded
    {snapshot.datetime} snapshot uploaded
    ...
    {user.name} uploaded
    >>>
    ```

- `upload_thought`

    This function sends a given thought of a given user id to the server.
    You may also provide an address (host and port) which the function send the information to (defaults are set to ``'127.0.0.1'`` and ``5000``, respectfully). 

    ```pycon
    >>> from brain_computer_interface.client import upload_thought
    >>> upload_thought(user_id=1, thought='I think therefore I am', host='127.0.0.1', port=5000)
    done!
    >>>
    ```

## Command Line Interface

The `brain_computer_interface.client` package also provides a command-line interface.
```sh
    $ python -m brain_computer_interface.client [OPTIONS] COMMAND [ARGS]
```

The top-level options include:

- ``-q``, ``--quiet``

    This option suppresses the output.

- ``-t``, ``--traceback``

    This option shows the full traceback when an exception is raised (by
    default, only the error message is printed, and the program exits with a
    non-zero code).

Commands:

- `read`

    Receives mind path and prints its contents in a humanly fashion.

    ```sh
    $ python -m brain_computer_interface.client read [OPTIONS] PATH
    ```

    Options:
    - ``--help``                  Show similar message and exit.

- `upload-mind`

    Receives mind path and uploads it to the server.

    ```sh
    $ python -m brain_computer_interface.client upload-mind [OPTIONS] PATH
    ```

    Options:
    - ``-h``, ``--host`` TEXT     [default: 127.0.0.1]
    - ``-p``, ``--port`` INTEGER  [default: 5000]
    - ``--help``                  Show similar message and exit.

- `upload-thought`

    Receives user id and though, and uploads it to the server.

    ```sh
    $ python -m brain_computer_interface.client upload-thought [OPTIONS] USER_ID THOUGHT
    ```

    Options:
    - ``-h``, ``--host`` TEXT     [default: 127.0.0.1]
    - ``-p``, ``--port`` INTEGER  [default: 5000]
    - ``--help``                  Show similar message and exit.

- `error`

    Raises an exception and prints it to the screen.

    ```sh
    $ python -m brain_computer_interface.client error [OPTIONS]
    ```

    Options:
    - ``--help``                  Show similar message and exit.

All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

To showcase these options, consider `error` command, which raises an exception:

```sh
$ python -m brain_computer_interface.client error
ERROR: something went terribly wrong :[
$ python -m brain_computer_interface.client -q error  # suppress output
$ python -m brain_computer_interface.client -t error  # show full traceback
ERROR: something went terribly wrong :[
Traceback (most recent call last):
    ...
RuntimeError: something went terrible wrong :[
```

Do note that each command's options should be passed to *that* command, for example the `-q` and `-t` options should be passed to `brain_computer_interface.client`, not `upload-mind` or `upload-thought`.

```sh
$ python -m brain_computer_interface.client upload-mind -q  # this doesn't work
ERROR: no such option: -q
$ python -m brain_computer_interface.client -q upload-mind  # this does work
```

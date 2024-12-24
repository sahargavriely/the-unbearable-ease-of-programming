# brain-computer-interface.parser

Sub-package of brain-computer-interface.
The following package allows one to parse snapshot.

For further information take a look at [full documentation](https://the-unbearable-ease-of-programming.readthedocs.io/en/latest/parser/parser.html).

## Usage

The `brain_computer_interface.parser` packages provides the following functions:

- `parse`

    This function receive parser name and raw data; and returns parsed data.
    You may also provide a shared directory - the directory where large information is located.

    ```pycon
    >>> from brain_computer_interface.parser import parse
    >>> data = dict(metadata=dict(user_id=1, datetime=0),
                    data=dict(rotation=dict(w=0.4, x=0.1, y=0.2, z=0.3),
                              translation=dict(x=0.1, y=0.2, z=0.3)))
    >>> parse('feelings', data, shared_dir='shared/')
    {'metadata': {'user_id': 1, 'datetime': 0}, 
     'data': {'rotation': {'w': 0.4, 'x': 0.1, 'y': 0.2, 'z': 0.3},
              'translation': {'x': 0.1, 'y': 0.2, 'z': 0.3}}}
    >>>
    ```

## Command Line Interface

The `brain_computer_interface.parser` package also provides a command-line interface.
```sh
    $ python -m brain_computer_interface.parser [OPTIONS] COMMAND [ARGS]
```

The top-level options include:

- ``-q``, ``--quiet``

    This option suppresses the output.

- ``-t``, ``--traceback``

    This option shows the full traceback when an exception is raised (by
    default, only the error message is printed, and the program exits with a
    non-zero code).

Command:

- `parse`

    Receives parser name and path to file a file with a raw snapshot data; and the parsed data.

    ```sh
    $ python -m brain_computer_interface.parser parse [OPTIONS] NAME DATA_PATH
    ```

    Options:
    - ``-s``, ``--shared-dir`` PATH  [default: shared]
    - ``--help``                     Show similar message and exit.

- `run-parser`

    Receives parser name and running a service which listens to the parser subscribe handle.

    ```sh
    $ python -m brain_computer_interface.parser run-parser [OPTIONS] NAME
    ```

    Options:
    - ``-s``, ``--shared-dir`` PATH        [default: shared]
    - ``-d``, ``--distribute-scheme`` TEXT [default: rabbitmq://localhost:5672/]
    - ``-g``, ``--group``
    - ``--help``                           Show similar message and exit.

- `error`

    Raises an exception and prints it to the screen.

    ```sh
    $ python -m brain_computer_interface.parser error [OPTIONS]
    ```

    Options:
    - ``--help``                  Show similar message and exit.

All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

To showcase these options, consider `error` command, which raises an exception:

```sh
$ python -m brain_computer_interface.parser error
ERROR: something went terribly wrong :[
$ python -m brain_computer_interface.parser -q error  # suppress output
$ python -m brain_computer_interface.parser -t error  # show full traceback
ERROR: something went terribly wrong :[
Traceback (most recent call last):
    ...
RuntimeError: something went terrible wrong :[
```

Do note that each command's options should be passed to *that* command, for example the `-q` and `-t` options should be passed to `brain_computer_interface.parser`, not `parse` or `run-parser`.

```sh
$ python -m brain_computer_interface.parser parse -q  # this doesn't work
ERROR: no such option: -q
$ python -m brain_computer_interface.parser -q parse  # this does work
```

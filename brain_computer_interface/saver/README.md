# brain-computer-interface.saver

Sub-package of brain-computer-interface.
The following package implements a saver who knows how to save data to the database component.

For further information take a look at [full documentation](https://the-unbearable-ease-of-programming.readthedocs.io/en/latest/saver/saver.html).

## Usage

The `brain_computer_interface.saver` packages provides the following function:


- `Saver(url: str)`

    This class exposes functionality.
    It receives url which is being used to load the corresponding database driver from [`drivers/`](/brain_computer_interface/database/drivers/) directory.
    The class support the following functinalities:

    - `save_user(self, user_id: int, data: dict)`

        Saves user's `data` of `uesr_id`.

    - `save_snapshot_topic(self, user_id: int, datetime: int, topic: str, data: dict)`

        Saves user's snapshot topic `data` of `topic`, `datetime` and `user_id`.
    
```pycon
>>> from brain_computer_interface.saver import Saver
>>> saver = Saver('scheme_of_some_driver://...')
>>> saver.save_user(42, {'name': 'Sahar', 'birthday': ...})
>>> saver.save_snapshot_topic(42, 0, 'pose', {'translation': ..., 'rotation': ...})
```

## Command Line Interface

The `brain_computer_interface.saver` package also provides a command-line interface.
```sh
    $ python -m brain_computer_interface.saver [OPTIONS] COMMAND [ARGS]
```

The top-level options include:

- ``-q``, ``--quiet``

    This option suppresses the output.

- ``-t``, ``--traceback``

    This option shows the full traceback when an exception is raised (by
    default, only the error message is printed, and the program exits with a
    non-zero code).

Commands:

- ``save``

    Top level command which supports ``snapshot`` and ``user`` from file.

    - ``user``

        Saves user information from the PATH to USER_ID.

        ```sh
        $ brain_computer_interface.saver save user [OPTIONS] USER_ID PATH
        ```
        Options:
        - ``-d``, ``--database`` TEXT            [default: postgresql://postgres:password@127.0.0.1:5432/mind]
        - ``--help``                             Show this message and exit.

    - ``snapshot``

        Saves snapshot's TOPIC information from the PATH to USER_ID and DATETIME.

        ```sh
        $ brain_computer_interface.saver save snapshot [OPTIONS] USER_ID DATETIME TOPIC PATH
        ```
        Options:
        - ``-d``, ``--database`` TEXT            [default: postgresql://postgres:password@127.0.0.1:5432/mind]
        - ``--help``                             Show this message and exit.

- ``run-saver``

    Runs the saver which listen to ``parsed`` data and user data and saves them to the database.

    ```sh
    $ python -m brain_computer_interface.saver run-saver [OPTIONS]
    ```
    Options:
    - ``-d``, ``--database`` TEXT            [default: postgresql://postgres:password@127.0.0.1:5432/mind]
    - ``-ds``, ``--distribute-scheme`` TEXT  [default: rabbitmq://localhost:5672/]
    - ``--help``                             Show this message and exit.

- `error`

    Raises an exception and prints it to the screen.

    ```sh
    $ python -m brain_computer_interface.saver error [OPTIONS]
    ```

    Options:
    - ``--help``                  Show similar message and exit.

All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

To showcase these options, consider `error` command, which raises an exception:

```sh
$ python -m brain_computer_interface.saver error
ERROR: something went terribly wrong :[
$ python -m brain_computer_interface.saver -q error  # suppress output
$ python -m brain_computer_interface.saver -t error  # show full traceback
ERROR: something went terribly wrong :[
Traceback (most recent call last):
    ...
RuntimeError: something went terrible wrong :[
```

Do note that each command's options should be passed to *that* command, for example the `-q` and `-t` options should be passed to `brain_computer_interface.saver`, not `run-saver`.

```sh
$ python -m brain_computer_interface.saver run-saver -q  # this doesn't work
ERROR: no such option: -q
$ python -m brain_computer_interface.saver -q run-saver  # this does work
```

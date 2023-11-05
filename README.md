[![codecov](https://codecov.io/gh/sahargavriely/the-unbearable-ease-of-programming/graph/badge.svg?token=W0V7MR7T8S)](https://codecov.io/gh/sahargavriely/the-unbearable-ease-of-programming)

# brain-computer-interface

A brain-computer-interface (BCI), a direct communication pathway between the brain's electrical activity and an external device, most commonly a computer or robotic limb.
The following package allows to run two servers, a server which receives __thoughts__ and a webserver to make those accessible.
The package also supplies a client to upload a __thoughts__.


For further information take a look at [full documentation](https://brain-computer-interface.readthedocs.io/en/latest/).


## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:sahargavriely/the-unbearable-ease-of-programming.git
    ...
    $ cd the-unbearable-ease-of-programming/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [brain-computer-interface] $  # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:

    ```sh
    $ pytest tests/
    ...
    ```


## Usage

The `brain_computer_interface` packages provides the following functions:

- `run_server`

    This function starts the server which receives thoughts from users.
    You may provide an address (host and port) which the server listens to (defaults are set to ``'0.0.0.0'`` and ``5000``, respectfully) a directory in which the server will save the thoughts to (default is set to ``data/``). 

    ```pycon
    >>> from brain_computer_interface import run_server
    >>> from pathlib import Path
    >>> run_server(host='0.0.0.0', port=5000, data_dir=Path('data/'))

    ```

- `run_webserver`

    This function starts the webserver which makes the users' thoughts accessible.
    You may provide an address (host and port) which the webserver listens to (defaults are set to ``'0.0.0.0'`` and ``8000``, respectfully) a directory in which the server will save the thoughts to (default is set to ``data/``). 

    ```pycon
    >>> from brain_computer_interface import run_webserver
    >>> from pathlib import Path
    >>> run_webserver(host='0.0.0.0', port=8000, data_dir=Path('data/'))
    * Serving Flask app "brain_computer_interface.webserver.webserver" (lazy loading)
    * Environment: production
      WARNING: This is a development server. Do not use it in a production deployment.
      Use a production WSGI server instead.
    * Debug mode: on
    * Running on http://127.0.0.1:8000/ (Press CTRL+C to quit)

    ```

- `upload_thought`

    This function sends a given thought of a given user id to the server.
    You may also provide an address (host and port) which the function send the information to (defaults are set to ``'127.0.0.1'`` and ``5000``, respectfully). 

    ```pycon
    >>> from brain_computer_interface import upload_thought
    >>> upload_thought(user_id=1, thought='I think therefore I am', host='127.0.0.1', port=5000)
    done!
    >>>
    ```


## Command Line Interface

The `brain_computer_interface` package also provides a command-line interface.
```sh
    $ python -m brain_computer_interface [OPTIONS] COMMAND [ARGS]
```

The top-level options include:

- ``-q``, ``--quiet``

    This option suppresses the output.

- ``-t``, ``--traceback``

    This option shows the full traceback when an exception is raised (by
    default, only the error message is printed, and the program exits with a
    non-zero code).

To see the version, do the following:

```sh
$ python -m brain_computer_interface --version
brain_computer_interface, version 0.1.0
```

- ``run-server``

    Runs the server which listens to thoughts.

    ```sh
    $ python -m brain_computer_interface run-server [OPTIONS]
    ```
    Options:
    - ``-h``, ``--host`` TEXT      [default: 0.0.0.0]
    - ``-p``, ``--port`` INTEGER   [default: 5000]
    - ``-d``, ``--data_dir`` PATH  [default: data]
    - ``-D``, ``--debug``
    - ``--help``                   Show similar message and exit.

- `run-webserver`

    Runs the webserver which makes the users' thoughts accessible.

    ```sh
    $ python -m brain_computer_interface run-webserver [OPTIONS]
    ```
    Options:
    - ``-h``, ``--host`` TEXT      [default: 0.0.0.0]
    - ``-p``, ``--port`` INTEGER   [default: 8000]
    - ``-d``, ``--data_dir`` PATH  [default: data]
    - ``-D``, ``--debug``
    - ``--help``                   Show similar message and exit.

- `upload-thought`

    Receives user id and though, and uploads it to the server.

    ```sh
    $ python -m brain_computer_interface upload-thought [OPTIONS] USER_ID THOUGHT
    ```

    Options:
    - ``-h``, ``--host`` TEXT     [default: 127.0.0.1]
    - ``-p``, ``--port`` INTEGER  [default: 5000]
    - ``--help``                  Show similar message and exit.

- `error`

    Raises an exception and prints it to the screen.

    ```sh
    $ python -m brain_computer_interface error [OPTIONS]
    ```

    Options:
    - ``--help``                  Show similar message and exit.

All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

To showcase these options, consider `error` command, which raises anexception:

```sh
$ python -m brain_computer_interface error
ERROR: something went terribly wrong :[
$ python -m brain_computer_interface -q error  # suppress output
$ python -m brain_computer_interface -t error  # show full traceback
ERROR: something went terribly wrong :[
Traceback (most recent call last):
    ...
RuntimeError: something went terrible wrong :[
```

Do note that each command's options should be passed to *that* command, for example the `-q` and `-t` options should be passed to `brain_computer_interface`, not `run_server`, `run-webserver` or `upload-thought`.

```sh
$ python -m brain_computer_interface run-server -q  # this doesn't work
ERROR: no such option: -q
$ python -m brain_computer_interface -q run-server  # this does work
```

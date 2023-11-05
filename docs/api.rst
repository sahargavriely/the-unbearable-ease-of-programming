brain_computer_interface API Reference
======================================

This is brain_computer_interface's API reference.


run_server
----------

.. function:: brain_computer_interface.run_server

    This function starts the server which receives thoughts from users.
    You may provide an address (host and port) which the server listens to (defaults are set to ``'0.0.0.0'`` and ``5000``, respectfully) a directory in which the server will save the thoughts to (default is set to ``data/``).

    .. method:: run_server(host='0.0.0.0', port=5000, data_dir=Path('data/'))


run_webserver
-------------

.. function:: brain_computer_interface.run_webserver

    This function starts the webserver which makes the users' thoughts accessible.
    You may provide an address (host and port) which the webserver listens to (defaults are set to ``'0.0.0.0'`` and ``8000``, respectfully) a directory in which the server will save the thoughts to (default is set to ``data/``). 

    .. method:: run_webserver(host='0.0.0.0', port=8000, data_dir=Path('data/'))


upload_thought
--------------

.. function:: brain_computer_interface.upload_thought

    This function sends a given thought of a given user id to the server.
    You may also provide an address (host and port) which the function send the information to (defaults are set to ``'127.0.0.1'`` and ``5000``, respectfully). 

    .. method:: upload_thought(user_id=1, thought='I think therefore I am', host='127.0.0.1', port=5000)
   
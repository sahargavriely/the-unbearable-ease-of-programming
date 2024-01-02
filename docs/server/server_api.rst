API Reference
=============

This is brain_computer_interface.server's API reference.

run_server
----------

.. function:: run_server(host='0.0.0.0', port=5000, shared_dir=Path('data/'))

    This function starts the server which receives thoughts from users.
    You may provide an address (host and port) which the server listens to (defaults are set to ``'0.0.0.0'`` and ``5000``, respectfully) a directory in which the server will save the thoughts to (default is set to ``data/``).

API Reference
=============

This is brain_computer_interface.server's API reference.

run_server
----------

.. function:: run_server(publish_method, host='0.0.0.0', port=5000, shared_dir=Path('shared/'))

    This function starts the server which receives minds from clients and forward them to ``publish_method`` - a publish function e.g. ``publish_method=print`` the data will be printed to the screen.
    You may provide an address (host and port) which the server listens to (defaults are set to ``'0.0.0.0'`` and ``5000``, respectfully) a directory in which the server will save the thoughts to (default is set to ``shared/``).

API Reference
=============

This is brain_computer_interface.rest's API reference.

run_rest_server
---------------

.. function:: run_rest_server(host='0.0.0.0', port=5000, database_scheme='postgresql://postgres:password@127.0.0.1:5432/mind')

    This function starts the rest server which exposes a restfull api.
    You may provide an address (host and port) which the rest listens to (defaults are set to ``'0.0.0.0'`` and ``5000``, respectfully) and a database scheme (default is set to ``postgresql://postgres:password@127.0.0.1:5432/mind``).

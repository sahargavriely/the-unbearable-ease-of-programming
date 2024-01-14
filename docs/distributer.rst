Distributer Reference
=====================

The distributer package responsible for distributing data in between the inner system parts.

And exposes the Distributer class.

Distributer:
------------

.. _target to distributer:

.. class:: Distributer(url: str)

    This class defines distribute functionality.
    It receives url which is being used to load the corresponding distribute driver from `drivers/ <https://github.com/sahargavriely/the-unbearable-ease-of-programming/blob/main/brain_computer_interface/distributer/drivers/>`_ directory.

.. _target to publish:

    .. method:: publish(self, data, topic)

        Publish `data` to `topic`.
        `data` must be in JSON format (we want to support many drivers).

.. _target to subscribe:

    .. method:: subscribe(self, callback, *topics, subscriber_group='')

        Subscribe to `topics` and upon receiving data calling the `callback` with the received data (in JSON format) as an argument.
        `subscriber_group` argument meant to enable distribute work between different subscribers which are part of the same group, empty group means every subscriber will get the same work.

    .. method:: connect(self)

        Returns and calls directly to the driver's `connect` is exists.
        Used also as the `enter` part of `Distributer`'s `with` statement.

    .. method:: close(self)

        Returns and calls directly to the driver's `close` is exists.
        Used also as the `exit` part of `Distributer`'s `with` statement.

    .. method:: publish_server(self, data)

        Publish user information by :ref:`publish_user <target to publish_user>` __or__ snapshot information by :ref:`publish_raw_snapshot <target to publish_raw_snapshot>` if possible.
        `data` must be in JSON format (we want to support many drivers).

.. _target to publish_user:

    .. method:: publish_user(self, data)

        Publish user information to `user` topic.
        `data` must be in JSON format (we want to support many drivers).

.. _target to publish_raw_snapshot:

    .. method:: publish_raw_snapshot(self, data)

        Publish `data` to `raw.X` where X is every possible topic in a snapshot.
        `data` must be in JSON format (we want to support many drivers).

    .. method:: publish_parsed_topic(self, parsed_topic_data, topic)

        Publish `data` to `f'parsed.{topic}'`.
        `parsed_topic_data` must be in JSON format (we want to support many drivers).

    .. method:: subscribe_parsed_topic(self, callback, topic, subscriber_group='')

        Subscribe to `f'parsed.{topic}'` and upon receiving data calling the `callback` with the received data (in JSON format) as an argument.
        `subscriber_group` argument meant to enable distribute work between different subscribers which are part of the same group, empty group means every subscriber will get the same work.

    .. method:: subscribe_raw_topic(self, callback, topic, subscriber_group='')

        Subscribe to `f'raw.{topic}'` and upon receiving data calling the `callback` with the received data (in JSON format) as an argument.
        `subscriber_group` argument meant to enable distribute work between different subscribers which are part of the same group, empty group means every subscriber will get the same work.

*Developers Note*
-----------------

To added a new driver all you have to do is:

1. Implement :ref:`publish <target to publish>` and :ref:`subscribe <target to subscribe>` methods.

2. Add a `scheme` class attribute that will be used to locate your newly driver, by :ref:`run-server <target to run-server>` command.

3. Finally add your driver under `drivers/ <https://github.com/sahargavriely/the-unbearable-ease-of-programming/blob/main/brain_computer_interface/distributer/drivers/>`_.

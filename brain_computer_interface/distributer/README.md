# brain-computer-interface.distributer

Sub-package of brain-computer-interface.
The following package responsible for distributing data in between the inner system parts.

For further information take a look at [full documentation](https://the-unbearable-ease-of-programming.readthedocs.io/en/latest/distributer.html).

## Usage

The `brain_computer_interface.distributer` packages provides the Distributer class:

- `Distributer(url: str)`

    This class defines distribute functionality.
    It receives url which is being used to load the corresponding distribute driver from [`drivers/`](/brain_computer_interface/distributer/drivers/) directory.
    Each driver should support minimum of the following two bound methods which are also `Distributer`'s bound methods and are directly calling to driver's one.

    - `publish(self, data, topic)`

        Publish `data` to `topic`.
        `data` must be in JSON format (we want to support many drivers).

    - `subscribe(self, callback, topic, subscriber_group='')`

        Subscribe to `topic` and upon receiving data calling the `callback` with the received data (in JSON format) as an argument.
        `subscriber_group` argument meant to enable distribute work between different subscribers which are part of the same group, empty group means every subscriber will get the same work.

    Continuing with `Distributer` bound methods:

    - `connect(self)`

        Returns and calls directly to the driver's `connect` is exists.
        Used also as the `enter` part of `Distributer`'s `with` statement

    - `close(self)`

        Returns and calls directly to the driver's `close` is exists.
        Used also as the `exit` part of `Distributer`'s `with` statement

    - `publish_raw_snapshot(self, data)`

        Publish `data` to `raw.X` where X is every possible topic in a snapshot.
        `data` must be in JSON format (we want to support many drivers).

    - `publish_parsed_topic(self, parsed_topic_data, topic)`

        Publish `data` to `f'parsed.{topic}'`.
        `parsed_topic_data` must be in JSON format (we want to support many drivers).

    - `subscribe_parsed_topic(self, callback, topic, subscriber_group='')`

        Subscribe to `f'parsed.{topic}'` and upon receiving data calling the `callback` with the received data (in JSON format) as an argument.
        `subscriber_group` argument meant to enable distribute work between different subscribers which are part of the same group, empty group means every subscriber will get the same work.

    - `subscribe_raw_topic(self, callback, topic, subscriber_group='')`

        Subscribe to `f'raw.{topic}'` and upon receiving data calling the `callback` with the received data (in JSON format) as an argument.
        `subscriber_group` argument meant to enable distribute work between different subscribers which are part of the same group, empty group means every subscriber will get the same work.

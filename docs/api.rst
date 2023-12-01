brain_computer_interface API Reference
======================================

This is brain_computer_interface's API reference.


run_server
----------

.. function:: run_server(host='0.0.0.0', port=5000, data_dir=Path('data/'))

    This function starts the server which receives thoughts from users.
    You may provide an address (host and port) which the server listens to (defaults are set to ``'0.0.0.0'`` and ``5000``, respectfully) a directory in which the server will save the thoughts to (default is set to ``data/``).


run_webserver
-------------

.. function:: run_webserver(host='0.0.0.0', port=8000, data_dir=Path('data/'))

    This function starts the webserver which makes the users' thoughts accessible.
    You may provide an address (host and port) which the webserver listens to (defaults are set to ``'0.0.0.0'`` and ``8000``, respectfully) a directory in which the server will save the thoughts to (default is set to ``data/``). 


.. _target to upload_mind:

upload_mind
-----------

.. function:: upload_mind(mind_path, host='127.0.0.1', port=5000)

    This function sends a given :ref:`mind file <target to mind file>` to the server.
    You may also provide an address (host and port) which the function send the information to (defaults are set to ``'127.0.0.1'`` and ``5000``, respectfully). 


upload_thought
--------------

.. function:: upload_thought(user_id, thought, host='127.0.0.1', port=5000)

    This function sends a given thought (*string*) of a given user id (*int*) to the server.
    You may also provide an address (host and port) which the function send the information to (defaults are set to ``'127.0.0.1'`` and ``5000``, respectfully).


.. _target to color image:

ColorImage
----------

.. class:: ColorImage(width, height, data)

    Holds a color image information from the user's mind.
    `data` is bytes object with the length of `width` * `height` * 3 (RBG).


.. _target to depth image:

DepthImage
----------

.. class:: DepthImage(width, height, data)

    Holds a depth image information from the user's mind.
    `data` is a list of floats with the length of `width` * `height`.


.. _target to feelings:

Feelings
--------

.. class:: Feelings(hunger, thirst, exhaustion, happiness)

    Holds feelings information from the user's mind.
    All arguments are floats.


.. _target to rotation:

Rotation
--------

.. class:: Rotation(x, y, z, w)

    Holds rotation information from the user's mind.
    All arguments are floats.


.. _target to translation:

Translation
-----------

.. class:: Translation(x, y, z)

    Holds rotation information from the user's mind.
    All arguments are floats.


.. _target to pose:

Pose
----

.. class:: Pose(translation, rotation)

    Holds position information from the user's mind.
    `translation` is a :ref:`Translation <target to translation>` object.
    `rotation` is a :ref:`Rotation <target to rotation>` object.


.. _target to snapshot:

Snapshot
--------

.. class:: Snapshot(datetime, pose, color_image, depth_image, feelings)

    Holds snapshot information from the user's mind.
    `datetime` is an *int* type like timestamp from epoch but in milliseconds.
    `pose` is a :ref:`Pose <target to pose>` object.
    `color_image` is a :ref:`ColorImage <target to color image>` object.
    `depth_image` is a :ref:`DepthImage <target to depth image>` object.
    `feelings` is a :ref:`Feelings <target to feelings>` object.

    .. method:: serialize(self)

        Serialize the snapshot into a bytes like object.

    .. method:: from_bytes(cls, bytes)

        A class method which gets a bytes like object and returns a :ref:`Snapshot <target to snapshot>` object



.. _target to user:

User
----

.. class:: User(id, name, birthday, gender)

    Holds user information.
    `id` the user id as an *int*,
    `name` the user name as a *string*,
    `birthday` the user birthday since epoch,
    `gender` the user gender *0* for male, *1* for female and *2* for other

    .. method:: serialize(self)

        Serialize the user into a bytes like object.

    .. method:: from_bytes(cls, bytes)

        A class method which gets a bytes like object and returns a :ref:`User <target to user>` object

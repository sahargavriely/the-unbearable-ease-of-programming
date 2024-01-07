brain_computer_interface Message Reference
==========================================

The message encapsulating the concept of mind as a data and defines how the on going messages in the system look like.

We start by describing the general features of every class that is part of our message; and continuing by describing the classes.

Methods:
--------

.. _target to jsonify:

.. method:: jsonify(self, path=None) -> dict

    Takes all the data in the class and returns it as a dictionary.
    The path argument is for saving un-jsonify properties to the given path directory.
    If path is `None` return a dict that doesn't necessarily qualifies as json.

.. _target to serialize:

.. method:: serialize(self) -> bytes

    Return the serialized form of the instance.

Classmethods:
-------------

.. _target to from_json:

.. classmethod:: from_json(cls, json_obj: dict)

    Receives a dictionary like :ref:`jsonify <target to jsonify>` returns and return an instance of the class.

.. _target to from_bytes:

.. classmethod:: from_bytes(cls, bytes: bytes)

    Receives a bytes like :ref:`serialize <target to serialize>` returns and return an instance of the class.

Classes:
--------

All can be imported from ``brain-computer-interface.message``

.. _target to color image:

.. class:: ColorImage(width, height, data)

    Holds a color image information from the user's mind.
    `data` is bytes object with the length of `width` * `height` * 3 (RBG).
    Note :ref:`jsonify <target to jsonify>`, :ref:`serialize <target to serialize>`, :ref:`from_json <target to from_json>` and :ref:`from_bytes <target to from_bytes>`

.. _target to depth image:

.. class:: DepthImage(width, height, data)

    Holds a depth image information from the user's mind.
    `data` is a list of floats with the length of `width` * `height`.
    Note :ref:`jsonify <target to jsonify>`, :ref:`serialize <target to serialize>`, :ref:`from_json <target to from_json>` and :ref:`from_bytes <target to from_bytes>`

.. _target to feelings:

.. class:: Feelings(hunger, thirst, exhaustion, happiness)

    Holds feelings information from the user's mind.
    All arguments are floats.
    Note :ref:`jsonify <target to jsonify>`, :ref:`serialize <target to serialize>`, :ref:`from_json <target to from_json>` and :ref:`from_bytes <target to from_bytes>`

.. _target to rotation:

.. class:: Rotation(x, y, z, w)

    Holds rotation information from the user's mind.
    All arguments are floats.
    Note :ref:`jsonify <target to jsonify>`, :ref:`serialize <target to serialize>`, :ref:`from_json <target to from_json>` and :ref:`from_bytes <target to from_bytes>`

.. _target to translation:

.. class:: Translation(x, y, z)

    Holds rotation information from the user's mind.
    All arguments are floats.
    Note :ref:`jsonify <target to jsonify>`, :ref:`serialize <target to serialize>`, :ref:`from_json <target to from_json>` and :ref:`from_bytes <target to from_bytes>`

.. _target to pose:

.. class:: Pose(translation, rotation)

    Holds position information from the user's mind.
    `translation` is a :ref:`Translation <target to translation>` object.
    `rotation` is a :ref:`Rotation <target to rotation>` object.
    Note :ref:`jsonify <target to jsonify>`, :ref:`serialize <target to serialize>`, :ref:`from_json <target to from_json>` and :ref:`from_bytes <target to from_bytes>`

.. _target to snapshot:

.. class:: Snapshot(datetime, pose, color_image, depth_image, feelings)

    Holds snapshot information from the user's mind.
    `datetime` is an *int* type like timestamp from epoch but in milliseconds.
    `pose` is a :ref:`Pose <target to pose>` object.
    `color_image` is a :ref:`ColorImage <target to color image>` object.
    `depth_image` is a :ref:`DepthImage <target to depth image>` object.
    `feelings` is a :ref:`Feelings <target to feelings>` object.
    Note :ref:`jsonify <target to jsonify>`, :ref:`serialize <target to serialize>`, :ref:`from_json <target to from_json>` and :ref:`from_bytes <target to from_bytes>`

.. _target to user:

.. class:: User(id, name, birthday, gender)

    Holds user information.
    `id` the user id as an *int*,
    `name` the user name as a *string*,
    `birthday` the user birthday since epoch,
    `gender` the user gender *0* for male, *1* for female and *2* for other
    Note :ref:`jsonify <target to jsonify>`, :ref:`serialize <target to serialize>`, :ref:`from_json <target to from_json>` and :ref:`from_bytes <target to from_bytes>`

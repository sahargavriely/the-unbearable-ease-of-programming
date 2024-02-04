Database Reference
==================

The database package responsible for distributing data in between the inner system parts.

And exposes the Database class.

Database
--------

.. _target to database:

.. class:: Database(url: str)

    This class defines load and save functionality.
    It receives url which is being used to load the corresponding database driver from [`drivers/`](/brain_computer_interface/database/drivers/) directory.
    Each driver should support the following bound methods which are also `Database`'s bound methods and are directly calling to driver's one.

.. _target to save_user:

    .. method:: save_user(self, user_id: int, data: dict)

        Saves user's `data` of `uesr_id`.

.. _target to save_snapshot_topic:

    .. method:: save_snapshot_topic(self, user_id: int, datetime: int, topic: str, data: dict)

        Saves user's snapshot topic `data` of `topic`, `datetime` and `user_id`.

.. _target to get_users:

    .. method:: get_users(self) -> list

        Returns a list with all users id.

.. _target to get_user:

    .. method:: get_user(self, user_id: int) -> dict

        Returns the corresponding data of `user_id`.

.. _target to get_user_snapshots:

    .. method:: get_user_snapshots(self, user_id: int) -> list

        Returns a list with all snapshots datetime of `user_id`.

.. _target to get_user_snapshot:

    .. method:: get_user_snapshot(self, user_id: int, datetime: int) -> dict

        Returns the corresponding data of `user_id` and `datetime`.

.. _target to get_user_snapshot_topic:

    .. method:: get_user_snapshot_topic(self, user_id: int, datetime: int, topic: str) -> dict

        Returns the corresponding data of `user_id`, `datetime` and `topic`.

.. _target to drop_db:

    .. method:: drop_db(self)

        Cleans/deletes the database.

*Developers Note*
-----------------

To added a new driver all you have to do is:

1. Implement all the above methods.

2. Add a `scheme` class attribute which will be used to locate your newly created driver.

3. Finally put your driver under `drivers/ <https://github.com/sahargavriely/the-unbearable-ease-of-programming/blob/main/brain_computer_interface/database/drivers/>`_.

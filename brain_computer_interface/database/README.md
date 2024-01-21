# brain-computer-interface.database

Sub-package of brain-computer-interface.
The following package responsible for data managing in the system.

For further information take a look at [full documentation](https://the-unbearable-ease-of-programming.readthedocs.io/en/latest/database.html).

## Usage

The `brain_computer_interface.database` packages provides the Database class:

- `Database(url: str)`

    This class defines load and save functionality.
    It receives url which is being used to load the corresponding database driver from [`drivers/`](/brain_computer_interface/database/drivers/) directory.
    Each driver should support the following bound methods which are also `Database`'s bound methods and are directly calling to driver's one.

    - `save_user(self, user_id: int, data: dict)`

        Saves user's `data` of `uesr_id`.

    - `save_snapshot_topic(self, user_id: int, datetime: int, topic: str, data: dict)`

        Saves user's snapshot topic `data` of `topic`, `datetime` and `user_id`.

    - `get_users(self) -> list`

        Returns a list with all users id.

    - `get_user(self, user_id: int) -> dict`

        Returns the corresponding data of `user_id`.

    - `get_user_snapshots(self, user_id: int) -> list`

        Returns a list with all snapshots datetime of `user_id`.

    - `get_user_snapshot(self, user_id: int, datetime: int) -> dict`

        Returns the corresponding data of `user_id` and `datetime`.

    - `get_user_snapshot_topic(self, user_id: int, datetime: int, topic: str) -> dict`

        Returns the corresponding data of `user_id`, `datetime` and `topic`.

    - `drop_db(self)`

        Cleans/deletes the database.

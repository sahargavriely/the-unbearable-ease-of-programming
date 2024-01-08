# brain-computer-interface.message

Sub-package of brain-computer-interface.
The following package encapsulating the concept of mind as a data and defines how the on going messages in the system look like.

For further information take a look at [full documentation](https://the-unbearable-ease-of-programming.readthedocs.io/en/latest/mind_file.html).

## Usage

The `brain_computer_interface.message` packages provides the following classes:

- `Snapshot`

    This class defines what a user's mind-snapshot is.
    Consists of datetime, pose (rotation and transition) of the user head in 3-dimensional space, color image from the mind eyes, depth image specifying the distance of every pixel in the color image and feelings.

- `User`

    This class defines a user.
    Consists of id, name, birthday and gender.

Every class has the following methods:

- `jsonify(self, path=None) -> dict`

    Takes all the data in the class and returns it as a dictionary.
    The path argument is for saving un-jsonify properties to the given path directory.
    If path is `None` you will receive the class as dict that doesn't necessarily qualifies as json.

- `serialize(self) -> bytes`

    Return the serialized form of the instance.

Every class has the following class methods:

- `from_json(cls, json_obj: dict)`

    Receives a dictionary like the one `jsonify` returns and return an instance of the class.

- `from_bytes(cls, bytes: bytes)`

    Receives a bytes like the one `serialize` returns and return an instance of the class.

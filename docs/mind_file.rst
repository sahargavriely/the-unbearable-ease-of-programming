.. _target to mind file:

Mind File Reference
===================

Since we are still lacking the hardware to connect to a real mind we have establish mind files.
Mind file simulates an actual mind processed into a file.

Mind files contain user information, the same information specified in the :ref:`User <target to user>` object,
and one or more snapshots information, the same information specified in the :ref:`Snapshot <target to snapshot>` object.

Usage
-----

Mind file can be stream to the server via :ref:`upload_mind <target to upload_mind>` function
or via :ref:`upload-mind <target to upload-mind>` command.
Mind file can be also be printed in a humanly fashion to the screen with the :ref:`read <target to read>` command.

Construct Your Own Mind
-----------------------

There can be many ways (currently two) to save a mind file.

One way to create a mind file, is to start with creating a :ref:`User <target to user>` object,
serialize it and dump its length as a *uint32* followed by the return value from the serialize method to a file.
Continue to do the same thing (serialize, dump its length follow by the serialized value) but with a :ref:`Snapshot <target to snapshot>` object (as many as you want).
Finally, compress your newly created mind file, but make sure its extension is *.gz*, so our system will know how to read it.
Voila we have a mind file.

*Developers Note*
-----------------

Once we can put our hands on a proper hardware we should be able to transmit user information without mind files, using other drivers.
To use other driver we can:

1. Look at the `drivers <https://github.com/sahargavriely/the-unbearable-ease-of-programming/blob/main/brain_computer_interface/reader/drivers.py>`_ choose one that suffices your needs and save accordingly.

2. Another option would be to add your own driver to `drivers <https://github.com/sahargavriely/the-unbearable-ease-of-programming/blob/main/brain_computer_interface/reader/drivers.py>`_, that suffices the following code-block.

    .. code-block:: python

        @collect_driver('distinguish_extension_for_the_driver')
        class DriverExample:
            def __init__(self, path: str):
                pass

            def open(self) -> StreamObjectExample:
                pass

            def read_user(self, stream: StreamObjectExample) -> User:
                pass

            def read_snapshot(self, stream: StreamObjectExample) -> Snapshot:
                pass


        class StreamObjectExample:
            def tell(self):  # returns a representation of the current stream location
                pass

            def seek(self, stream_location):  # returns stream from the asked location
                pass

            def peek(self, location: int):  # returns nothing if the stream ended
                pass

            def close(self):
                pass

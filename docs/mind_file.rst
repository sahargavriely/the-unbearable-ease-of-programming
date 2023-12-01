.. _target to mind file:

Mind File Reference
===================

Since we are still lacking the hardware to connect to a real mind we have establish mind files.
Mind file simulates an actual mind in a form of a file,
the file then can be stream to the server via :ref:`upload_mind <target to upload_mind>` function
or via :ref:`upload-mind <target to upload-mind>` command.
The file can be also printed in a humanly fashion to the screen with the :ref:`read <target to read>` command.

Mind files contain user information, the same information specified in the :ref:`User <target to user>` object,
and one or more snapshots information, the same information specified in the :ref:`Snapshot <target to snapshot>` object.

To create a mind file, start with creating a :ref:`User <target to user>` object,
serialize it and dump its length as a *uint32* followed by the return value from the serialize method to a file.
Continue to do the same thing but with a :ref:`Snapshot <target to snapshot>` object (as many as you want).
Voila we have a mind file.

You can also compress your newly created mind file, but make sure its extension is *.gz*, so we know it's a compressed type.

Note: uncompressed mind file has a unique encoding, now deprecated and soon to be removed.

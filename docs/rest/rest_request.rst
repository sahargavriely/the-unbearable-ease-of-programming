HTTP Request Reference
======================


Once the rest server is up and running, one execute the following http request at the address the server is on.

GET ``/users/<int:id>``
-----------------------

    Get the user information.

GET ``/users/<int:id>/snapshots/<int:datetime>``
------------------------------------------------

    Get the user's snapshot information.

GET ``/users/<int:id>/snapshots/<int:datetime>/<string:topic>``
---------------------------------------------------------------

    Get the user's snapshot's topic information.

GET ``/users/<int:id>/snapshots/<int:datetime>/<string:topic>/data``
--------------------------------------------------------------------

    Get the user's snapshot's topic's data (available for `color_image` and `depth_image`).

GET ``/users/<int:id>/snapshots``
---------------------------------

    Get the user's snapshots.

GET ``/users``
--------------

    Get all users.

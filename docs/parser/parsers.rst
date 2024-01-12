.. _target to parsers:

Parsers Reference
=================

Here you can find all the available information parsers.
Location, all parsers are located under `parsers <https://github.com/sahargavriely/the-unbearable-ease-of-programming/blob/main/brain_computer_interface/parser/parsers.py>`_.
Every parser is define by a function or a class that receives the data its subscribe to, and three attributes:
1. name.
2. subscribe - the data which the parser will receives.
3. publish - where the parser will forward the parsed data to.

The (currently) existing parsers are:


Color Image:
------------

.. attribute:: name
    :no-index:
    
    `'color_image'`


.. attribute:: subscribe
    :no-index:
    
    `'raw.color_image'`


.. attribute:: publish
    :no-index:
    
    `'parsed.color_image'`


Depth Image:
------------

.. attribute:: name
    :no-index:
    
    `'depth_image'`


.. attribute:: subscribe
    :no-index:
    
    `'raw.depth_image'`


.. attribute:: publish
    :no-index:
    
    `'parsed.depth_image'`


Feelings:
---------

.. attribute:: name
    :no-index:
    
    `'feelings'`


.. attribute:: subscribe
    :no-index:
    
    `'raw.feelings'`


.. attribute:: publish
    :no-index:
    
    `'parsed.feelings'`


Pose:
-----

.. attribute:: name
    :no-index:
    
    `'pose'`


.. attribute:: subscribe
    :no-index:
    
    `'raw.pose'`


.. attribute:: publish
    :no-index:
    
    `'parsed.pose'`


*Developers Note*
-----------------

To added a new parser all you have to do is:

1. Implement a function that starts with `parse_` or a class the ends with `Parser` and has a method by the name of `parse`.
   Both the function and the method should receive `data` as the first argument.
   (optional) Both the function and the method can receive `img_dir` as an argument, a shared directory which contains the raw images data.

2. (optional) Add `name` attribute, else the name of the parser will be define as the name of the function (without the `parse_` prefix) and in case of a class, the name will be define as the name of the class (without the `Parser` suffix).

3. (optional) Add `subscribe` attribute, else the parser will be subscribe to `f'raw.{parser.name}''`.

4. (optional) Add `publish` attribute, else the parser will be publish to `f'parsed.{parser.name}''`.

5. Put it all under `parsers <https://github.com/sahargavriely/the-unbearable-ease-of-programming/blob/main/brain_computer_interface/parser/parsers.py>`_.
   You will also can find examples in that file.

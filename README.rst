Flags
=================

A small no-requirements package for making bitwise flags in Python.

Installing
-----------------

Available on PyPi:

.. code:: sh

    pip install -U vf-flags

To install off of Github you can do the following

.. code:: sh

    pip install -U git+https://github.com/Voxel-Fox-Ltd/Flags

Quick Example
-----------------

.. code:: py

    import flags

    class WebsitePermissions(flags.Flags):

        @flags.flag_value
        def view_posts(self): return 0b001

        @flags.flag_value
        def edit_posts(self): return 0b010

        @flags.flag_value
        def delete_posts(self): return 0b100

    perms1 = WebsitePermissions(0b011)  # Init with a value
    perms1.view_posts  # True
    perms1.delete_posts  # False

    perms2 = WebsitePermissions(delete_posts=True)  # Init with kwargs
    perms2.view_posts  # False
    perms2.delete_posts  # True

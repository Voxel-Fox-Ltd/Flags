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

Here's a basic example of creating a flags class using decorators.

.. code:: py

    import vfflags

    class WebsitePermissions(vfflags.Flags):

        @vfflags.flag_value
        def view_posts(self):
            """If the user can view posts."""
            return 0b001

        @vfflags.flag_value
        def edit_posts(self):
            """If the user can edit posts."""
            return 0b010

        @vfflags.flag_value
        def delete_posts(self):
            return 0b100

Here's an alternative way to create a flags class using a class attribute.

.. code:: py

    import vfflags

    class WebsitePermissions(vfflags.Flags):

        # You can optionally add a docstring by adding your value to a tuple
        CREATE_FLAGS = {
            "view_posts": (0b001, "If the user can view posts."),
            "edit_posts": (0b010, "If the user can edit posts."),
            "delete_posts": 0b100,
        }

Here's the usage of either of the above.

.. code:: py

    perms1 = WebsitePermissions(0b011)  # Init with a value
    perms1.view_posts  # True
    perms1.delete_posts  # False

    perms2 = WebsitePermissions(delete_posts=True)  # Init with kwargs
    perms2.view_posts  # False
    perms2.delete_posts  # True

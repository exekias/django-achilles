"""
Achilles provides a framework to create Django applications using AJAX. Trough
the use of some primitives it allows you to build asynchronous without the need
of writting javascript to manage client side.
"""

__version__ = (0, 0, 9)


def get_version():
    """
    Get current version as a string (ie: '1.0.0')
    """
    return '.'.join([str(x) for x in __version__])

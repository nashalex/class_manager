def get_courses():
    """TODO: Docstring for get_classes.

    Parameters
    ----------
    arg1 : TODO

    Returns
    -------
    TODO

    """


class ClasesDescriptor(object):

    """Descriptor that manages the classes attribute of Manager"""

    def __get__(self, instance, owner):
        pass

    def __set__(self, instance, value):
        pass

    def __delete__(self, instance):
        pass


class Manager(object):

    """Manages all Classes"""

    def __init__(self):
        """Create a Mananger """

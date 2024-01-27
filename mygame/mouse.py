
__hovered = None
__last_hovered = None
__held = None
__last_held = None

def get_hovered():
    """Get item hovered by mouse, can be called from inside or outside the main module"""
    return __hovered

def get_held():
    """Get item held by mouse, can be called from inside or outside the main module"""
    return __held

def get_last_hovered():
    """Get item last hovered by mouse, can be called from inside or outside the main module"""
    return __last_hovered

def get_last_held():
    """Get item last held by mouse, can be called from inside or outside the main module"""
    return __last_held

def set_hovered(item):
    """Set item hovered by mouse, can be called from inside or outside the main module"""
    global __hovered, __last_hovered
    if __hovered is not None:
        __last_hovered = __hovered
    __hovered = item

def set_held(item):
    """Set item held by mouse, can be called from inside or outside the main module"""
    global __held, __last_held
    if __held is not None:
        __last_held = __held
    __held = item

class Mouse:
    """Create a mygame mouse object to store hovered and held items"""

    def __init__(self):
        """"Initialise a mouse object"""
        self.__hovered = None
        self.__last_hovered = None
        self.__held = None
        self.__last_held = None

    def get_hovered(self):
        """Get item hovered by mouse"""
        return self.__hovered

    def get_held(self):
        """Get item held by mouse"""
        return self.__held

    def get_last_hovered(self):
        """Get item last hovered by mouse"""
        return self.__last_hovered

    def get_last_held(self):
        """Get item last held by mouse"""
        return self.__last_held

    def set_hovered(self, item):
        """Set item hovered by mouse"""
        if self.__hovered is not None:
            self.__last_hovered = self.__hovered
        self.__hovered = item

    def set_held(self, item):
        """Set item held by mouse"""
        if self.__held is not None:
            self.__last_held = self.__held
        self.__held = item

# class Mouse:
#     """Create a mygame mouse object to store hovered and held items"""

#     def __init__(self):
#         """"Initialize a mouse object"""
#         self.__hovered = None
#         self.__last_hovered = None
#         self.__held = None
#         self.__last_held = None

#     @property
#     def hovered(self):
#         """Get item hovered by mouse"""
#         return self.__hovered

#     @property
#     def held(self):
#         """Get item held by mouse"""
#         return self.__held

#     @property
#     def last_hovered(self):
#         """Get item last hovered by mouse"""
#         return self.__last_hovered

#     @property
#     def last_held(self):
#         """Get item last held by mouse"""
#         return self.__last_held

#     @hovered.setter
#     def hovered(self, item):
#         """Set item hovered by mouse"""
#         if self.__hovered is not None:
#             self.__last_hovered = self.__hovered
#         self.__hovered = item

#     @held.setter
#     def held(self, item):
#         """Set item held by mouse"""
#         if self.__held is not None:
#             self.__last_held = self.__held
#         self.__held = item

"""
Item class for Jaseci

Each item has an id, name, timestamp.
"""
from jaseci.element.element import Element


class Item(Element):
    """Item class for Jaseci"""

    def __init__(self, value=None, **kwargs):
        self.item_value = value
        Element.__init__(self, **kwargs)

    @property
    def value(self):
        return self.item_value

    @value.setter
    def value(self, val):
        self.item_value = val
        self.save()

    def __str__(self):
        if self.value:
            return super().__str__() + f":{self.value}"
        else:
            return super().__str__() + ":None"


"""
Jac's set class for Jaseci

Adds relevant operators to id_list for operations on sets of nodes and edges
"""
# from jaseci.utils.id_list import id_list
from jaseci.utils.utils import logger
from jaseci.element.element import element


class jac_set(list):
    """
    Jac set class for operations in Jac lang
    """

    def __init__(self, in_list=None):
        if (in_list):
            for i in in_list:
                self.append(i)

    def append(self, item):
        if(not isinstance(item, element) or not hasattr(item, 'anchor_value')):
            logger.error(
                f"Invalid {type(item)} object {item} to be added to jac_set!")
        else:
            list.append(self, item)

    def add_obj(self, item):
        self.append(item)

    def obj_list(self):
        return self

    def __lt__(self, other):
        """Returns reduced set where anchor value evals to other"""
        ret = jac_set()
        for i in self:
            if (i.anchor_value() < other):
                ret.add_obj(i)
        return ret

    def __gt__(self, other):
        """Returns reduced set where anchor value evals to other"""
        ret = jac_set()
        for i in self:
            if (i.anchor_value() > other):
                ret.add_obj(i)
        return ret

    def __le__(self, other):
        """Returns reduced set where anchor value evals to other"""
        ret = jac_set()
        for i in self:
            if (i.anchor_value() <= other):
                ret.add_obj(i)
        return ret

    def __ge__(self, other):
        """Returns reduced set where anchor value evals to other"""
        ret = jac_set()
        for i in self:
            if (i.anchor_value() >= other):
                ret.add_obj(i)
        return ret

    def __eq__(self, other):
        """Returns reduced set where anchor value evals to other"""
        ret = jac_set()
        for i in self:
            if (i.anchor_value() == other):
                ret.add_obj(i)
        return ret

    def __ne__(self, other):
        """Returns reduced set where anchor value evals to other"""
        ret = jac_set()
        for i in self:
            if (i.anchor_value() != other):
                ret.add_obj(i)
        return ret

    def __add__(self, other):
        """Returns new set with operation applied"""
        ret = jac_set()
        for i in self:
            ret.add_obj(i)
        for i in other:
            if (i not in ret):
                ret.add_obj(i)
        return ret

    def __sub__(self, other):
        """Returns new set with operation applied"""
        ret = jac_set()
        for i in self:
            if(i not in other):
                ret.add_obj(i)
        return ret

    def __mul__(self, other):
        """Returns new set with operation applied, mul is intersection"""
        ret = jac_set()
        for i in self:
            if(i in other):
                ret.add_obj(i)
        return ret

    def __truediv__(self, other):
        """Returns new set with operation applied, div is 'outersection'"""
        ret = jac_set()
        for i in self:
            if(i not in other):
                ret.add_obj(i)
        for i in other:
            if(i not in self):
                ret.add_obj(i)
        return ret

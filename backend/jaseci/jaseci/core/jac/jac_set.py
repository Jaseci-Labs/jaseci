
"""
Jac's set class for Jaseci

Adds relevant operators to id_list for operations on sets of nodes and edges
"""
from core.utils.id_list import id_list
from core.utils.utils import logger


class jac_set(id_list):
    """
    Jac set class for operations in Jac lang
    """

    def is_valid(self):
        for i in self.obj_list():
            if ('anchored' not in dir()):
                logger.error(
                    str(f'{type(i)} in {self.owner_obj} not anchored'))
                return False
            return True

    def __lt__(self, other):
        """Returns reduced set where anchor value evals to other"""
        ret = jac_set(self.owner_obj)
        for i in self.obj_list():
            if (i.anchor_value() < other):
                ret.add_obj(i)
        return ret

    def __gt__(self, other):
        """Returns reduced set where anchor value evals to other"""
        ret = jac_set(self.owner_obj)
        for i in self.obj_list():
            if (i.anchor_value() > other):
                ret.add_obj(i)
        return ret

    def __le__(self, other):
        """Returns reduced set where anchor value evals to other"""
        ret = jac_set(self.owner_obj)
        for i in self.obj_list():
            if (i.anchor_value() <= other):
                ret.add_obj(i)
        return ret

    def __ge__(self, other):
        """Returns reduced set where anchor value evals to other"""
        ret = jac_set(self.owner_obj)
        for i in self.obj_list():
            if (i.anchor_value() >= other):
                ret.add_obj(i)
        return ret

    def __eq__(self, other):
        """Returns reduced set where anchor value evals to other"""
        ret = jac_set(self.owner_obj)
        for i in self.obj_list():
            if (i.anchor_value() == other):
                ret.add_obj(i)
        return ret

    def __ne__(self, other):
        """Returns reduced set where anchor value evals to other"""
        ret = jac_set(self.owner_obj)
        for i in self.obj_list():
            if (i.anchor_value() != other):
                ret.add_obj(i)
        return ret

    def __add__(self, other):
        """Returns new set with operation applied"""
        ret = jac_set(self.owner_obj)
        for i in self.obj_list():
            ret.add_obj(i)
        for i in other.obj_list():
            if (i not in ret.obj_list()):
                ret.add_obj(i)
        return ret

    def __sub__(self, other):
        """Returns new set with operation applied"""
        ret = jac_set(self.owner_obj)
        for i in self.obj_list():
            if(i not in other.obj_list()):
                ret.add_obj(i)
        return ret

    def __mul__(self, other):
        """Returns new set with operation applied, mul is intersection"""
        ret = jac_set(self.owner_obj)
        for i in self.obj_list():
            if(i in other.obj_list()):
                ret.add_obj(i)
        return ret

    def __truediv__(self, other):
        """Returns new set with operation applied, div is 'outersection'"""
        ret = jac_set(self.owner_obj)
        for i in self.obj_list():
            if(i not in other.obj_list()):
                ret.add_obj(i)
        for i in other.obj_list():
            if(i not in self.obj_list()):
                ret.add_obj(i)
        return ret

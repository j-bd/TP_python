"""Manage ordered dictionary with methodes such as sort and reverse"""

class DictionnaireOrdonne(dict):
    """Class inheriting of dict class"""


    def __add__(self, obj_to_add):
        """Add two dict"""
        sum_result = [x for x in self.items()] + [x for x in obj_to_add.items()]
        return {x[0]:x[1] for x in sum_result}


    def sort(self):
        """Sort the dict object"""
        list_tuple_sort = sorted([x for x in self.items()])
        return {x[0]:x[1] for x in list_tuple_sort}


    def reverse(self):
        """Reverse the dict object"""
        list_tuple_rev = reversed([x for x in self.items()])
        return {x[0]:x[1] for x in list_tuple_rev}

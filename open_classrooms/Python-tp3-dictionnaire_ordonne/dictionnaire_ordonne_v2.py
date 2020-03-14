"""Manage ordered dictionary with methodes such as sort and reverse"""

class DictionnaireOrdonne():
    """Class to create ordered dictionary"""

    def __init__(self, data={}, **args):
        """Initialization of the object"""
        self._keys = []
        self._values = []

        if (isinstance(data, dict) or isinstance(data, DictionnaireOrdonne)) is False:
            raise TypeError(f"The date type in parameters is {type(data)}" +
                            " but dict or DictionnaireOrdonne type is expected")

        for key in data:
            self[key] = data[key]

        for key in args:
            self[key] = args[key]


    def __setitem__(self, key, value):
        """Methode to fuel the object with data"""
        if key in self._keys:
            self._values[self._keys.index(key)] = value
        else:
            self._keys.append(key)
            self._values.append(value)


    def __getitem__(self, key):
        """Methode to obtain the value of a key"""
        if key not in self._keys:
            raise ValueError(f"{key} is not in the dictionary")
        else:
            return self._values[self._keys.index(key)]


    def __delitem__(self, key):
        """Methode to delete an item"""
        if key not in self._keys:
            raise ValueError(f"This item does not exist")
        else:
            index = self._keys.index(key)
            self._values.pop(index)
            self._keys.pop(index)


    def __repr__(self):
        """Methode to display the object"""
        string = "{"
        begin = True
        for k in self._keys:
            if begin:
                string += repr(self._keys[0]) + ": " + repr(self._values[0])
                begin = False
            else:
                string += ", " + repr(k) + ": " + repr(self._values[self._keys.index(k)])
        return string + "}"


    def __str__(self):
        """Methode used with function built in print"""
        return repr(self)


    def __len__(self):
        """Methode returning the size of data"""
        return len(self._keys)


    def __contains__(self, key):
        """Methode to control the presence of a key"""
        return key in self._keys


    def __iter__(self):
        """Methode to get an iter object"""
        return iter(self._keys)


    def __add__(self, element):
        """Methode to add a dict object or a DictionnaireOrdonne object"""
        if isinstance(element, DictionnaireOrdonne) is False:
            raise TypeError(f"The date type in parameters is {type(element)}" +
                            " but DictionnaireOrdonne type is expected")
        result = DictionnaireOrdonne()
        result._keys = self._keys + element._keys
        result._values = self._values + element._values
        return result


    def reverse(self):
        """Methode to reverse the dict"""
        self._keys.reverse()
        self._values.reverse()


    def items(self):
        """Methode to display all elements of the object"""
        l = list()
        for x in range(0, len(self._keys)):
            tup = (self._keys[x], self._values[x])
            l.append(tup)
        return l


    def keys(self):
        """Methode to display all the keys of the object"""
        return self._keys


    def values(self):
        """Methode to display all the values of the object"""
        return self._values


    def sort(self):
        """Methode to return the oject sort by _keys"""
        list_keys_sort = sorted([(key, index) for index, key in enumerate(self._keys)])
        self._keys = [list_keys_sort[x][0] for x in range(0, len(list_keys_sort))]

        values_sort = [self._values[x[1]] for x in list_keys_sort]
        self._values = values_sort
        
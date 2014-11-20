# -*- coding: utf-8 -*-
from collections import MutableMapping as _MutableMapping


class Section(_MutableMapping):
    """A dict-like datatype mapping layer names to a list of (<offset>, <elevation>)
    data. Also contains info on section name and station. For example:

    Section("D157", decimal.Decimal(1234.56), {
            "Natural Ground": [(-10.0, 70.0), (0.0, 70.08), (10.0, 70.40)],
            "Excavation": [(-10.0, 70.0), (-10.0, 69.0), (10.0, 69.0), (10.0, 70.40)]})
    """
    def __init__(self, name=None, station=None, *args):
        self.data = dict()
        self.update(dict(*args))
        self.name = name

        # Maybe taking care of <station> type should not be done here.
        # Just making sure inconsistent datatypes will not exist in main program.
        import decimal
        from input import FLOAT_PREC

        decimal.getcontext().prec = FLOAT_PREC
        if not isinstance(station, decimal.Decimal):
            print "At section %s with station %s: " % (name, station)
            print "Changing the type of station from %s to %s" % (type(station), decimal.Decimal)
            station = decimal.Decimal(station)
        self.station = station

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)

# class Section(_MutableSequence):
#     """A list-like datatype containing tuple((<offset>, <elevation>))
#     elements.
#     """
#
#     def __init__(self, name=None, station=None, *args):
#         self.name = name
#         self.station = station
#         self.data = list()
#         self.extend(list(args))
#
#     def _check(self, v):
#         if not isinstance(v, tuple):
#             raise TypeError("Element of Section object MUST be a tuble")
#
#         if not len(v) == 2:
#             raise TypeError("Tuple element of Section object MUST be of length 2")
#
#         if (not isinstance(v[0], float)) or (not isinstance(v[1], float)):
#             raise TypeError("Tuple element of Section object MUST contain floats")
#
#     def __getitem__(self, i):
#         return self.data[i]
#
#     def __delitem__(self, i):
#         del self.data[i]
#
#     def __setitem__(self, i, v):
#         self._check(v)
#         self.data[i] = v
#
#     def __len__(self):
#         return len(self.data)
#
#     def __str__(self):
#         return str(self.data)
#
#     def insert(self, i, v):
#         self._check(v)
#         self.data.insert(i, v)

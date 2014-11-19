# -*- coding: utf-8 -*-

import decimal
from input import *
from datatypes import *

decimal.getcontext().prec = FLOAT_PREC


def readsection(f):
    """Read section data from a GRD file object <f> and
    return a <Section> object.
    """
    secname, station = f.readline().strip().split()  # ValueError is raised at EOF

    data = []
    line = f.readline().strip()
    while not line.startswith("*"):
        offset, elev = line.split()
        data.append((float(offset), float(elev)))
        line = f.readline().strip()

    return secname, decimal.Decimal(station), data

# Read section data from input files. Create the Section objects
# and map their stations to themselves
sections = {}
for lname, fname in LAYERS.items():
    with open(fname) as inpf:
        assert inpf.readline().strip().startswith("*")
        while True:
            try:
                secname, station, ldata = readsection(inpf)
                section = sections[station]  # May raise KeyError
                assert section.name == secname
                section[lname] = ldata

            except KeyError:
                section = Section(secname, station, {lname: ldata})
                #---------------------------------------------------------------
                # sections[station] = section
                # sections[station] = Section(secname, station, {lname: ldata})
                #---------------------------------------------------------------

            except ValueError:  # Raised at EOF
                break

# -*- coding: utf-8 -*-

from input import *
from datatypes import *


#------------------------------------------------------------------------------
def readsection(grd):
    """Read data of a single section from a GRD file object <grd> and return data
    needed to construct a <Section> object. A <decimal.Decimal> object is used to
    represent the station of the section because that value is going to be used
    as a key in the <sections> dictionary. In order for <key in sections> to be
    evaluated correctly at all times we need a float value that can be compared
    for equality in a consistent manner.
    """
    import decimal
    decimal.getcontext().prec = FLOAT_PREC

    secname, station = grd.readline().strip().split()  # ValueError is raised at EOF

    data = []
    line = grd.readline().strip()
    while not line.startswith("*"):
        offset, elev = line.split()
        data.append((float(offset), float(elev)))
        line = grd.readline().strip()

    return secname, decimal.Decimal(station), data


#------------------------------------------------------------------------------
def getsections():
    """Read all section data from every GRD file givven and store it in the
    corresponding <Section> object. At the same time map the <Section> objects
    to their <station> values.
    """
    sections = {}
    for lname, fname in LAYERS.items():
        with open(fname) as grd:
            assert grd.readline().strip().startswith("*")
            while True:
                try:
                    secname, station, ldata = readsection(grd)
                    section = sections[station]     # May raise KeyError. <station>
                    assert section.name == secname  # should NOT be a float!!!
                    section[lname] = ldata

                except KeyError:
                    sections[station] = Section(secname, station, {lname: ldata})

                except ValueError:  # Raised at EOF
                    break

    return sections

# Read section data from input files. GRD files contain data for a givven layer
# but all layer data need to be contained by the corresponding <Section> object.
sections = getsections()

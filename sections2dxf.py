# -*- coding: utf-8 -*-

from input import *
from datatypes import *
from collections import OrderedDict


#------------------------------------------------------------------------------
def grdsections(grd):
    """Iterate over a GRD file object <grd> and yield per section data needed to
    construct a <Section> object. A <decimal.Decimal> object is used to represent
    the station of the section because that value is going to be used as a key in
    the <sections> dictionary. In order for <key in sections> to be evaluated
    as expected at all times we need a proper number type.
    """
    import decimal
    decimal.getcontext().prec = FLOAT_PREC

    while True:
        try:
            secname, station = grd.readline().strip().split()  # ValueError at EOF

            data = []
            line = grd.readline().strip()
            while not line.startswith("*"):
                offset, elev = line.split()
                data.append((float(offset), float(elev)))
                line = grd.readline().strip()
            yield (secname, decimal.Decimal(station), data)

        except ValueError:  # Raised at EOF
            break


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
            for sectiondata in grdsections(grd):
                secname, station, ldata = sectiondata
                try:
                    section = sections[station]  # <station> should NOT be a float!
                    assert section.name == secname
                    section[lname] = ldata

                except KeyError:
                    sections[station] = Section(secname, station, {lname: ldata})

    return sections

# Read section data from input files. GRD files contain data for a givven layer
# but all layer data need to be contained by the corresponding <Section> object.
sections = OrderedDict(sorted(getsections().items(), key=lambda t: t[0]))
#------------------------------------------------------------------------------
# section = sections.values()[0]
# print section.name, section.station
# print "\n".join([(str(elem) + ": " + str(section[elem])) for elem in section.keys()])
#------------------------------------------------------------------------------

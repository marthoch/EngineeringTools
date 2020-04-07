#!/usr/bin/env python3
# pylint: disable=line-too-long,wrong-import-position,abstract-method,no-else-return
"""

# doctest
# old format defaults for test
>>> from EngineeringTools.quantities import qnt
>>> qnt.FORMAT_DEFAULT['totalWidth'] = 8
>>> qnt.FORMAT_DEFAULT['decimalPosition'] = 4
>>> qnt.FORMAT_DEFAULT['thousands_sep'] = ''
"""

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"

# $Source$

# run doctest, workaround relative import
if __name__ == '__main__':
    import sys
    import doctest # pylint: disable=import-outside-toplevel
    module_name = 'EngineeringTools.tools.geo_circle'          # pylint: disable=invalid-name
    module = __import__(module_name, fromlist=['*'], level=0)  # pylint: disable=invalid-name
    module._setup_doctest()                                    # pylint: disable=protected-access
    print(doctest.testmod(module, optionflags=doctest.ELLIPSIS))
    sys.exit()

# $Source$

from .. import quantities as ETQ
from EngineeringTools.tools.functions import sqrt


class Circle:
    """Circle

    @param keyword: use one of the following keywords as parameter
        ['radius', 'r', 'diameter', 'd', 'area', 'A', 'perimeter', 'U']
    @type  keyword: quantities.Distance / quantities.Area; UVal; float

    U{http://en.wikipedia.org/wiki/Circle}

    >>> print(Circle(diameter=ETQ.Distance(20.0, 'mm')))
    Circle(radius=10.000 mm (Distance))
    >>> print(Circle(diameter=ETQ.Distance(20.0, 'mm').uval))
    Circle(radius=0.01000 {m})
    >>> print(Circle(diameter=20.0))
    Circle(radius=10.0)
    >>> print(Circle(diameter=ETQ.Force(20.0, 'N').uval))
    Circle(radius=10.00 {kg m s^-2})
    >>> print(repr(Circle(radius=ETQ.Distance(10.0, 'mm'))))
    Circle(radius=quantities.Distance(value=0.01, unit='m', displayUnit='mm'))
    >>> print(Circle(radius=ETQ.Distance(10.0, 'mm')).area)
     314     mm^2 (Area)
    >>> print(Circle(area=ETQ.Area(1.0, 'm^2')).diameter)
    1128.379 mm (Distance)
    >>> print(Circle(area=Circle(diameter=ETQ.Distance(1.0, 'mm')).area).diameter)
       1.000 mm (Distance)
    >>> print(Circle(d=Circle(area=ETQ.Area(1.0, 'mm^2')).diameter).area)
       1.000 mm^2 (Area)

    """
    def __init__(self, **vargsd):
        if len(vargsd) != 1:
            raise Exception("circle has one parameter: but not %s" % vargsd)

        key, value = vargsd.popitem()
        self._retQuantitiy = False
        if isinstance(value, ETQ.QuantityNumeric):
            value = value.uval
            self._retQuantitiy = True
        if key in ('radius', 'r'):
            self._radius = value
        elif key in ('diameter', 'd'):
            self._radius = value / 2.0
        elif key in ('area', 'A'):
            self._radius = sqrt(value / ETQ.PI)
        elif key in ('perimeter', 'U'):
            self._radius = value / (2.0 * ETQ.PI)
        elif key in ('momentOfAreaSecond', 'I'):
            self._radius = (value *4. / ETQ.PI)**(1, 4)
        else:
            raise Exception("parameter not known: %s" % vargsd)


    def __str__(self):
        return 'Circle(radius=%s)' % str(self.radius).strip()


    def __repr__(self):
        return 'Circle(radius=%r)' % self.radius


    diameter = property(fget=lambda self: ETQ.Distance(2.0 * self._radius) if self._retQuantitiy else 2.0 * self._radius)
    d = diameter
    area = property(fget=lambda self: ETQ.Area(self._radius **2 * ETQ.PI) if self._retQuantitiy else self._radius **2 * ETQ.PI)
    A = area
    perimeter = property(fget=lambda self: ETQ.Distance(self._radius * 2.0 * ETQ.PI) if self._retQuantitiy else self._radius * 2.0 * ETQ.PI)
    U = perimeter
    radius = property(fget=lambda self: ETQ.Distance(self._radius) if self._retQuantitiy else self._radius)
    r = radius


################################################################################
# test
################################################################################
def _setup_doctest():
    ETQ.Quantity.set_displayUnitSystem('mechanicalEngineering')

#eof

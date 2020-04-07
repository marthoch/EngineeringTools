#!/usr/bin/env python3
# pylint: disable-msg=line-too-long,missing-module-docstring,missing-function-docstring,missing-class-docstring,no-else-return,invalid-name,multiple-statements

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"

__all__ = ["Sphere", ]

# $Source$
# run doctest, workaround relative import
if __name__ == '__main__':
    import sys
    import doctest # pylint: disable=import-outside-toplevel
    module_name = 'EngineeringTools.volume.volume'             # pylint: disable=invalid-name
    module = __import__(module_name, fromlist=['*'], level=0)  # pylint: disable=invalid-name
    module._setup_doctest()                                    # pylint: disable=protected-access
    print(doctest.testmod(module, optionflags=doctest.ELLIPSIS))
    sys.exit()

from .. import quantities as ETQ


class Sphere():

    def __init__(self, R=None, D=None):
        if R:
            self._radius = ETQ.Distance(R)
        elif D:
            self._radius = ETQ.Distance(D/2.)
        else:
            raise Exception("parameter not known")

    def __str__(self):
        return 'Sphere(radius={})'.format(str(self.radius).strip())

    def __repr__(self):
        return 'Sphere(radius={})'.format(repr(self.radius))

    def get_mass(self, density):
        return ETQ.Mass(self.volume * density)

    volume =  property(fget=lambda self: ETQ.Volume(4./3.*self.radius **3 * ETQ.PI))

    radius =  property(fget=lambda self: ETQ.Distance(self._radius))
    R = radius


def _setup_doctest():
    ETQ.Quantity.set_displayUnitSystem('mechanicalEngineering')

#eof

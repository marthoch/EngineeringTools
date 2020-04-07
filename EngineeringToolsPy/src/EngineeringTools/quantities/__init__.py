#!/usr/bin/env python3
# pylint: disable=line-too-long,wrong-import-position,abstract-method,no-else-return

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"

# run doctest, workaround relative import
if __name__ == '__main__':
    import sys
    import doctest # pylint: disable=import-outside-toplevel
    import EngineeringTools.quantities as ETQ             # pylint: disable=import-self
    ETQ.Quantity.set_displayUnitSystem('mechanicalEngineering')
    module_name = 'EngineeringTools.quantities'      # pylint: disable=invalid-name
    module = __import__(module_name, fromlist=['*'], level=0)  # pylint: disable=invalid-name
    print(doctest.testmod(module, optionflags=doctest.ELLIPSIS))
    sys.exit()

from .. import qnt
from . import quantitiesbase as base
from .quantitiesbase import *
from . import mechanics
from .mechanics import *
from . import electrical
from .electrical import *

from ..tools import PI

def get_all_available_quantities():
    """Search and return all currently available (loaded) quantities
    """

    def get_derived_quantities(quantity):
        subcls = quantity.__subclasses__()
        qset = set()
        for subq in subcls:
            qset |= set((subq,))
            qset |= get_derived_quantities(subq)
        return qset
    return get_derived_quantities(Quantity)


def find_quantity_by_unit(unit):
    """Find all quantities which have a specific unit

    >>> from EngineeringTools import quantities as ETQ
    >>> sorted({a.__name__ for a in  ETQ.find_quantity_by_unit('N.m')})
    ['BendingMoment', 'Torque']
    """
    quantities = get_all_available_quantities()
    qwithunit = set()
    for quant in quantities:
        if unit in quant.get_units():
            qwithunit |= set((quant,))
    return qwithunit

# eof

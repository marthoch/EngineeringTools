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


__all__ = ["velocity_angular", "speed"]

# $Source$

# run doctest, workaround relative import
if __name__ == '__main__':
    import sys
    import doctest # pylint: disable=import-outside-toplevel
    module_name = 'EngineeringTools.tools.calc'                # pylint: disable=invalid-name
    module = __import__(module_name, fromlist=['*'], level=0)  # pylint: disable=invalid-name
    module._setup_doctest()                                    # pylint: disable=protected-access
    print(doctest.testmod(module, optionflags=doctest.ELLIPSIS))
    sys.exit()

from .. import quantities as ETQ
from ..uval import UVal


def velocity_angular(speed):
    """
    >>> print(velocity_angular(speed=ETQ.Speed(1500.0, 'rpm')))
     157     rad/sec (VelocityAngular)
    >>> print(velocity_angular(speed=ETQ.Speed(1500.0, 'rpm').uval))
     157     rad/sec (VelocityAngular)
    """
    if isinstance(speed, (ETQ.Speed, UVal)):
        return ETQ.VelocityAngular(2.0 * ETQ.PI * speed)
    else:
        raise Exception('wrong type of argument: %s' % speed)


def speed(velocity_angular):
    """
    >>> print(speed(velocity_angular=ETQ.VelocityAngular(157.0, 'rad/sec')))
    1500     rpm (Speed)
    >>> print(speed(velocity_angular=ETQ.VelocityAngular(157.0, 'rad/sec').uval))
    1500     rpm (Speed)
    """
    if isinstance(velocity_angular, (ETQ.VelocityAngular, UVal)):
        return ETQ.Speed(velocity_angular / (2.0 * ETQ.PI))
    else:
        raise Exception('wrong type of argument: %s' % speed)



################################################################################
# test
################################################################################
def _setup_doctest():
    ETQ.Quantity.set_displayUnitSystem('mechanicalEngineering')

#eof ###########################################################################


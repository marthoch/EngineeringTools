#!/usr/bin/env python3
# pylint: disable-msg=line-too-long,missing-module-docstring,missing-function-docstring,missing-class-docstring,no-else-return,invalid-name,multiple-statements,wrong-import-position

"""

# doctest
# old format defaults for test
>>> from EngineeringTools.quantities import qnt
>>> qnt.FORMAT_DEFAULT['totalWidth'] = 8
>>> qnt.FORMAT_DEFAULT['decimalPosition'] = 4
>>> qnt.FORMAT_DEFAULT['thousands_sep'] = ''
"""
from statsmodels.sandbox.distributions.sppatch import expect

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"

# run doctest, workaround relative import
if __name__ == '__main__':
    import sys
    import doctest # pylint: disable=import-outside-toplevel
    from EngineeringTools import quantities as ETQ             # pylint: disable=reimported,import-outside-toplevel
    ETQ.Quantity.set_displayUnitSystem('mechanicalEngineering')
    module_name = 'EngineeringTools.tools.functions'      # pylint: disable=invalid-name
    module = __import__(module_name, fromlist=['*'], level=0)  # pylint: disable=invalid-name
    module._setup_doctest()                                    # pylint: disable=protected-access
    print(doctest.testmod(module, optionflags=doctest.ELLIPSIS))
    sys.exit()

# $Source$

from fractions import Fraction
import numpy as _np
from .. import quantities as ETQ

################################################################################
#  exceptions
################################################################################
class EngineeringTools_tools_Error(Exception):
    """Exception: tools"""

class EngineeringTools_tools_Error_units(EngineeringTools_tools_Error):
    """Exception: tools"""


################################################################################
#  constants
################################################################################
PI = ETQ.Scalar(_np.pi, '1.0', displayUnit='1.0')


################################################################################
# functions
################################################################################
def sin(angle):
    """ sin

    >>> angle = ETQ.Angle(30.0, 'deg')
    >>> print(angle)
      30.000 deg (Angle)
    >>> print(round(sin(angle.get_value('rad')), 3))
    0.5
    >>> sin(angle.get_uval())
    UVal(0.49999999999999994, {})
    >>> print(sin(angle.get_uval()))
    0.5000 {}
    >>> print(sin(angle))
       0.500  (Scalar)
    >>> print(sin(ETQ.Distance(0.5, 'm')))
    Traceback (most recent call last):
        ...
    EngineeringTools.tools.functions.EngineeringTools_tools_Error_units: wrong type : <class 'EngineeringTools.quantities.mechanics.Distance'>

    """
    if isinstance(angle, float):
        return _np.sin(angle)
    elif isinstance(angle, ETQ.UVal):
        angle.check_units({})
        return ETQ.UVal(_np.sin(angle.get_value()), {})
    elif isinstance(angle, ETQ.Angle):
        return ETQ.Scalar(_np.sin(angle.get_value()))
    else:
        raise EngineeringTools_tools_Error_units('wrong type : %s' % type(angle))



def arcsin(scalar):
    """ arcsin

    >>> scalar = ETQ.Scalar(0.5, '1.0')
    >>> print(scalar)
       0.500  (Scalar)
    >>> print(asin(scalar.get_value()))  # rad
    0.52359877559...
    >>> asin(scalar.get_uval())
    UVal(0.5235987755982989, {})
    >>> print(asin(scalar.get_uval()))
    0.5236 {}
    >>> a=asin(scalar); a.set_displayUnit('deg'); print(a)
      30.000 deg (Angle)
    >>> print(asin(ETQ.Distance(0.5, 'm')))
    Traceback (most recent call last):
        ...
    EngineeringTools.tools.functions.EngineeringTools_tools_Error_units: wrong type : <class 'EngineeringTools.quantities.mechanics.Distance'>

    """
    if isinstance(scalar, float):
        return _np.arcsin(scalar)
    elif isinstance(scalar, ETQ.UVal):
        scalar.check_units({})
        return ETQ.UVal(_np.arcsin(scalar.get_value()), {})
    elif isinstance(scalar, ETQ.Scalar):
        return ETQ.Angle(_np.arcsin(scalar.get_value()), 'rad')
    else:
        raise EngineeringTools_tools_Error_units('wrong type : %s' % type(scalar))


asin = arcsin   # compatibility with math module


def cos(angle):
    """ cos

    >>> angle = ETQ.Angle(30.0, 'deg')
    >>> print(angle)
      30.000 deg (Angle)
    >>> print(cos(angle.get_value('rad')))
    0.866025403784...
    >>> cos(angle.get_uval())
    UVal(0.8660254037844387, {})
    >>> print(cos(angle.get_uval()))
    0.8660 {}
    >>> print(cos(angle))
       0.866  (Scalar)
    >>> print(cos(ETQ.Distance(0.5, 'm')))
    Traceback (most recent call last):
        ...
    EngineeringTools.tools.functions.EngineeringTools_tools_Error_units: wrong type : <class 'EngineeringTools.quantities.mechanics.Distance'>

    """
    if isinstance(angle, float):
        return _np.cos(angle)
    elif isinstance(angle, ETQ.UVal):
        angle.check_units({})
        return ETQ.UVal(_np.cos(angle.get_value()), {})
    elif isinstance(angle, ETQ.Angle):
        return ETQ.Scalar(_np.cos(angle.get_value()), '1.0')
    else:
        raise EngineeringTools_tools_Error_units('wrong type : %s' % type(angle))



def arccos(scalar):
    """ arccos

    >>> scalar = ETQ.Scalar(0.5, '1.0')
    >>> print(scalar)
       0.500  (Scalar)
    >>> print((arccos(scalar.get_value())))  # rad
    1.047197551...
    >>> print(arccos(scalar.get_uval()))
    1.047 {}
    >>> print(arccos(scalar.get_uval()))
    1.047 {}
    >>> a=arccos(scalar); a.set_displayUnit('deg'); print(a)
      60.000 deg (Angle)
    >>> print(arccos(ETQ.Distance(0.5, 'm')))
    Traceback (most recent call last):
        ...
    EngineeringTools.tools.functions.EngineeringTools_tools_Error_units: wrong type : <class 'EngineeringTools.quantities.mechanics.Distance'>

    """
    if isinstance(scalar, float):
        return _np.arccos(scalar)
    elif isinstance(scalar, ETQ.UVal):
        scalar.check_units({})
        return ETQ.UVal(_np.arccos(scalar.get_value()), {})
    elif isinstance(scalar, ETQ.Scalar):
        return ETQ.Angle(_np.arccos(scalar.get_value()), 'rad')
    else:
        raise EngineeringTools_tools_Error_units('wrong type : %s' % type(scalar))


acos = arccos  # compatibility with math module


def tan(angle):
    """ tan

    >>> angle = ETQ.Angle(30.0, 'deg')
    >>> print(angle)
      30.000 deg (Angle)
    >>> print(tan(angle.get_value('rad')))
    0.5773502691...
    >>> tan(angle.get_uval())
    UVal(0.5773502691896257, {})
    >>> print(tan(angle.get_uval()))
    0.5774 {}
    >>> print(tan(angle))
       0.577  (Scalar)
    >>> print(tan(ETQ.Distance(0.5, 'm')))
    Traceback (most recent call last):
        ...
    EngineeringTools.tools.functions.EngineeringTools_tools_Error_units: wrong type : <class 'EngineeringTools.quantities.mechanics.Distance'>

    """
    if isinstance(angle, float):
        return _np.tan(angle)
    elif isinstance(angle, ETQ.UVal):
        angle.check_units({})
        return ETQ.UVal(_np.tan(angle.get_value()), {})
    elif isinstance(angle, ETQ.Angle):
        return ETQ.Scalar(_np.tan(angle.get_value()), '1.0')
    else:
        raise EngineeringTools_tools_Error_units('wrong type : %s' % type(angle))



def atan(scalar):
    """ atan

    >>> scalar = ETQ.Scalar(0.5)
    >>> print(scalar)
       0.500  (Scalar)
    >>> print(atan(scalar.get_value()))  # rad
    0.46364760900...
    >>> print(atan(scalar.get_uval()))
      26.565 deg (Angle)
    >>> a=atan(scalar); a.set_displayUnit('deg'); print(a)
      26.565 deg (Angle)
    >>> print(atan(ETQ.Distance(0.5, 'm')))
    Traceback (most recent call last):
        ...
    EngineeringTools.tools.functions.EngineeringTools_tools_Error_units: wrong type : <class 'EngineeringTools.quantities.mechanics.Distance'>

    """
    if isinstance(scalar, float):
        return _np.arctan(scalar)
    elif isinstance(scalar, ETQ.UVal):
        scalar.check_units({})
        return ETQ.Angle(_np.arctan(scalar.get_value()), 'rad')
    elif isinstance(scalar, ETQ.Scalar):
        return ETQ.Angle(_np.arctan(scalar.get_value()), 'rad')
    else:
        raise EngineeringTools_tools_Error_units('wrong type : %s' % type(scalar))


def atan2(y, x):
    """ atan2

    >>> y = ETQ.Distance(1/3.0**(0.5), 'm')
    >>> x = ETQ.Distance(1.0, 'm')
    >>> print(y, x)
     577.350 mm (Distance) 1000.000 mm (Distance)
    >>> print(atan2(y, x))
      30.000 deg (Angle)
    >>> atan2(y.uval, x.uval)
    UVal(0.5235987755982989, {})
    >>> print(atan2(y.value, x.value) / _np.pi * 180.0)
    30.0...

    """
    if isinstance(y, float) and isinstance(x, float):
        return _np.arctan2(y, x)
    elif isinstance(y, ETQ.UVal) and isinstance(x, ETQ.UVal):
        y.check_units(x)
        return ETQ.UVal(_np.arctan2(y.get_value(), x.get_value()), {})
    elif y.match_quantities(x):
        return ETQ.Angle(_np.arctan2(y.get_value(), x.get_value()), 'rad')
    else:
        raise EngineeringTools_tools_Error_units('wrong type or combination : %s, %s' % (type(y), type(x)))


def sqrt(uvalue):
    """square root of uval, wurzel

        >>> uv = ETQ.UVal(9.0, {}); print(uv)
        9.000 {}
        >>> print(sqrt(uv))
        3.000 {}
        >>> print(sqrt(9.0))
        3.0

    """
    if isinstance(uvalue, ETQ.UVal):
        return pow(uvalue, (1, 2))
    elif  isinstance(uvalue, (float, int)):
        return uvalue**(1.0/2.0)
    elif isinstance(uvalue, ETQ.Quantity):
        return pow(uvalue.uval, (1, 2))
    else:
        raise EngineeringTools_tools_Error_units('type not recognized: {}'.format(type(uvalue)))


def sqrtSigned(val):
    """square root of uval, wurzel, keeping the sign

    >>> a = ETQ.Area(4, 'm2')
    >>> sqrtSigned(a)
    UVal(2.0, {'meter': Fraction(1, 1)})

    >>> a = ETQ.Area(-4, 'm2')
    >>> sqrtSigned(a)
    UVal(-2.0, {'meter': Fraction(1, 1)})

    """
    return val.sign()*sqrt(val.abs())


def log10(scalar):
    """log to basis 10
    """
    if isinstance(scalar, int):
        scalar = float(scalar)
    if isinstance(scalar, float):
        return _np.log10(scalar)
    elif isinstance(scalar, ETQ.UVal):
        scalar.check_units({})
        return ETQ.UVal(_np.log10(scalar.get_value()), {})
    else:
        raise EngineeringTools_tools_Error_units('type not recognized: {}'.format(type(scalar)))


def log(scalar):
    """log to basis e
    """
    if isinstance(scalar, int):
        scalar = float(scalar)
    if isinstance(scalar, float):
        return _np.log(scalar)
    elif isinstance(scalar, ETQ.UVal):
        scalar.check_units({})
        return ETQ.UVal(_np.log(scalar.get_value()), {})
    else:
        raise EngineeringTools_tools_Error_units('type not recognized: {}'.format(type(scalar)))


def exp(scalar):
    """exp
    """
    if isinstance(scalar, int):
        scalar = float(scalar)
    if isinstance(scalar, float):
        return _np.exp(scalar)
    elif isinstance(scalar, ETQ.UVal):
        scalar.check_units({})
        return ETQ.UVal(_np.exp(scalar.get_value()), {})
    else:
        raise EngineeringTools_tools_Error_units('type not recognized: {}'.format(type(scalar)))


def power(value, exp):
    """  value**exp
    """
    if isinstance(value, ETQ.QuantityNumeric):
        value = value.uval
    if isinstance(exp, (ETQ.Number, ETQ.Scalar)):
        exp = exp.get_value()

    if isinstance(exp, int):
        exp = float(exp)

    if isinstance(value, (float, int)) and isinstance(exp, float):
        return _np.power(value, exp)
    elif isinstance(value, ETQ.UVal) and isinstance(exp, float):
        units = {k:v*exp for k,v in value._units.items()}
        return ETQ.UVal(_np.power(value.get_value(), exp), units)
    else:
        raise EngineeringTools_tools_Error_units('type not recognized: {}, {}'.format(type(value), type(exp)))



def limitTo(x, limitLower, limitUpper):
    if x < limitLower:
        x = limitLower.set_properties_from(x)
    elif x > limitUpper:
        x = limitUpper.set_properties_from(x)
    return x


def physical_constants(name):
    """return a physical constant from sp.constants.physical_constants as uval
    """
    unittable = {'m':ETQ.UVal(1, {'meter':Fraction(1,1)}),
                 'K':ETQ.UVal(1, {'kelvin':Fraction(1,1)}),
                 'W':ETQ.Power(1, 'W').uval,
                 'Hz':ETQ.Frequency(1,'Hz').uval,
                 'ohm':ETQ.Resistance(1,'Ohm').uval}
    try:
        import scipy as _sp
        phConst = _sp.constants.physical_constants[name]
    except KeyError as e:
        raise e

    value = phConst[0]
    unitStr = phConst[1]
    ul = unitStr.split(' ')
    uval = ETQ.UVal(value, {})
    for ui in ul:
        ux = ui.split('^')
        if len(ux) < 2:
            ux.append(1)
        try:
            uval *= power(unittable[ux[0]], int(ux[1]))
        except KeyError:
            raise KeyError('{} : {}'.format(ux[0], ui))
    return uval


################################################################################
# test
################################################################################
def _setup_doctest():
    ETQ.Quantity.set_displayUnitSystem('mechanicalEngineering')

#eof

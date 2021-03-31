#!/usr/bin/env python3
# pylint: disable=line-too-long,no-else-return,missing-function-docstring,missing-class-docstring,empty-docstring
# pylint: disable=invalid-name,too-many-branches,no-else-raise,wrong-import-position,trailing-whitespace
"""physical quantities::

--------------------------------------------------------------------------------
content:
    A reasonable way to handle quantities and units.

    Build-in functionality to to write GUIs.

see:
    U{http://www.ptb.de/de/publikationen/download/}
    U{http://www.ptb.de/de/publikationen/download/pdf/si.pdf}
    U{http://en.wikipedia.org/wiki/Category:Physical_quantity}
--------------------------------------------------------------------------------

HowTo write units:
    - do only use 7-Bit-Chars
    - use ., ex: 'N.m', but not 'Nm'  ????
        do not use: 'N m', 'Nm'
    - use '^' for exponents
    - prefer the long version, avoid not very common abbreviation
    - The si-prefixes (see si.pdf p22) have the highest binding priority:
            km^2 =  1000^2 * m^2
        Prefix and unit symbol create a new symbol which will not be separated.
        do not use '*' for prefixes: m*sec  != 0.001sec
        si.pdf : "Vorsatzzeichen und Einheitenzeichen bilden ein neues,
        nicht trennbares Einheitenzeichen (das ein Vielfaches oder einen Teil
        der betreffenden Einheit ergibt), das mit anderen Einheitenzeichen
        kombiniert werden und positive oder negative Exponenten haben kann,
        um zusammengesetzte Einheitenzeichen zu bilden."

--------------------------------------------------------------------------------

FIXME: java-code-generator: automatic generation of java-quantities form python-quantities

FIXME: implementation of Quantity__dezimal

FIXME: better implementation of __str__
        configurable format
        fixed width with space padding, fixed position of the point

FIXME: min, max

--------------------------------------------------------------------------------

class Quantity(object) ... base class


--------------------------------------------------------------------------------

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
import numbers
import logging
import numpy as np
import numpy as _np

# run doctest, workaround relative import
if __name__ == '__main__':
    import sys
    import doctest                                                 # pylint: disable=import-outside-toplevel
    from EngineeringTools import quantities as ETQ                 # pylint: disable=reimported,import-outside-toplevel
    ETQ.Quantity.set_displayUnitSystem('mechanicalEngineering')
    module_name = 'EngineeringTools.quantities.quantitiesbase'     # pylint: disable=invalid-name
    module = __import__(module_name, fromlist=['*'], level=0)      # pylint: disable=invalid-name                                # pylint: disable=protected-access
    print(doctest.testmod(module, optionflags=doctest.ELLIPSIS))
    sys.exit()


from ..uval import UVal
from .. import qnt
from .. import quantities as ETQ


DEFAULT_STR_QUANTIZATION = {'method':'1r', 'precision':3}


################################################################################
#  exceptions
################################################################################
class ParaDInF_quantity_Error(Exception):
    """Exception: quantities"""

class ParaDInF_quantity_ErrorUnitNotFound(LookupError):
    """Exception: quantities: unit not found in units"""

class ParaDInF_quantity_ErrorQuantitiesDoNotMatch(Exception):
    """Exception: quantities do not match"""



################################################################################
#  functions
################################################################################

def generateQuantity(quantity, value, unit=None, displayUnit=None, typecast=False, **varargsd):
    """generate quantity object

    use this only to get the quantity form string or hash

    >>> from EngineeringTools.quantities.quantitiesbase import *
    >>> from EngineeringTools.quantities.mechanics import *

    >> L = generateQuantity('Distance', 27.3, 'mm')  # FIXIT:
    >> print(L)
      27.300 mm (Distance)

    >> dQ = {'quantity':'Force', 'value':122.0, 'unit':'kN', 'test':'nix'}
    >> qQ = generateQuantity(**dQ)
    >> print(qQ)
     122     kN (Force)

    @param quantity: name of quantity = name of class
    @type  quantity: str
    @param value: value
    @type  value: float, int, long, str ... according quantity
    @param unit: unit of value
    @type  unit: str
    @param displayUnit: unit to display value
    @type  displayUnit: str
    @param varargsd: only for compability

    """
    return eval(quantity + '(value=value, unit=unit, displayUnit=displayUnit, typecast=typecast)')


def _float_equal(fn1, fn2, epsilon=1e-8):
    """
    >>> print(_float_equal(0.1, 0.1))
    True
    >>> print(_float_equal(0.1, 0.2))
    False
    >>> print(_float_equal(0, 0))
    True
    >>> print(_float_equal(0.0, 0.00000001))
    False
    >>> print(_float_equal(0.0, 0.000000001))
    True
    """
    fn1 = float(fn1)
    fn2 = float(fn2)
    asum = abs(fn1) + abs(fn2)
    diff = abs(fn1 - fn2)
    if asum < epsilon:
        return True
    else:
        return (diff / asum) < epsilon


################################################################################
#  base classes
################################################################################
class Quantity:
    """Quantity base class"""

    _displayUnitSystem = None
    _displayUnitDefault = None
    _displayUnitSystemList = {}
        # example Distance:
        # {'mechanicalEngineering':{'displayUnit':'mm',
        #                           'str_quantization':{'method':'1', 'precision':3}}
    _isoUnit = '1'
    _units = {'1':1.0}
    _unitsPreferred = []     # list of preferred units ['m', 'mm', 'km']
    _uval_units = {}         # dict of units; see class UVal
    _str_quantization = None # {'method':'1r', 'precision':3}

    @classmethod
    def set_displayUnitSystem(cls, displayUnitSystem):
        """set the displayUnitSystem for all quantities
        """
        if displayUnitSystem in (None, 'mechanicalEngineering'):
            cls._displayUnitSystem = displayUnitSystem
            if  displayUnitSystem is None:
                cls._str_quantization = DEFAULT_STR_QUANTIZATION
            else:
                t = cls._displayUnitSystemList.get(cls._displayUnitSystem, None)
                if t:
                    cls._str_quantization = t.get('str_quantization', None)
                else:
                    cls._str_quantization = DEFAULT_STR_QUANTIZATION
            if (cls._str_quantization is None) and (displayUnitSystem in 'mechanicalEngineering'):
                cls._str_quantization = DEFAULT_STR_QUANTIZATION
        else:
            raise ParaDInF_quantity_Error('displayUnitSystem "%s" is not available' % displayUnitSystem)

    @classmethod
    def set_displayUnitDefault(cls, displayUnit):
        if displayUnit in cls._units.keys():
            cls._displayUnitDefault = displayUnit
        else:
            raise ParaDInF_quantity_Error('displayUnit "%s" is not available' % displayUnit)


    @classmethod
    def set_str_quantization(cls, method=None, precision=None):
        if method is None:
            cls._str_quantization = DEFAULT_STR_QUANTIZATION
        else:
            cls._str_quantization = {'method':method, 'precision':precision}


    def set_str_quantizationQ(self, method=None, precision=None):
        # TODO: get class method and method clearly separated
        if method is None:
            self._str_quantization = DEFAULT_STR_QUANTIZATION
        else:
            self._str_quantization = {'method':method, 'precision':precision}

    def __init__(self, value, unit=None, displayUnit=None, typecast=True):
        """q  =  Quantity(value, unit=iso, displayUnit=unit)

        value is converted from unit to iso-unit
        if no unit is specified, unit=iso
        if no displayUnit is specified, displayUnit=unit

        """
        self.log = logging.getLogger('ParaDIn.quantity')
        self.log.debug('quantitiy %s __init__ (%s (%s))', self.__class__.__name__, type(value), value)
        self._displayUnit = None
        if isinstance(value, Quantity):
            if isinstance(value, self.__class__):
                self._value = value.get_value()
                if displayUnit is None:
                    displayUnit = value.get_displayUnit()
            else:
                raise ParaDInF_quantity_ErrorQuantitiesDoNotMatch(
                    '%s != %s' % (self.__class__.__name__, value.get_quantity_name()))
        elif isinstance(value, UVal):
            if unit is None:
                value.check_units(self._uval_units)
                self._value = self.convert2iso(value.get_value(), self._isoUnit, typecast=True)
            else:
                raise ParaDInF_quantity_Error('when passing UVal, unit must be None')
        else:
            #if unit == None:
            #    unit = self._isoUnit
            if unit in self._units:
                self._value = self.convert2iso(value, unit, typecast=typecast)
            else:
                raise ParaDInF_quantity_ErrorUnitNotFound('unit "{:s}" is not available in {}. Use: {}'.format(str(unit), type(self), ', '.join(self._units.keys())))
        if not self._unitsPreferred:
            self._unitsPreferred = self._units  # not to class!; QuantityFloat(1.0); Time(1.0)
        self.set_displayUnit(displayUnit)


    def __str__(self, unit=None):
        """Quantity.__str__()

        string representation

        """
        if unit is None:
            unit = self._displayUnit
        value = self.convert2unit(self._value, unit)
        if self._str_quantization is None:
            return '{} {} ({})'.format(qnt.quant(value, rettype='string', **DEFAULT_STR_QUANTIZATION), unit, self.__class__.__name__)
        else:
            return '{} {} ({})'.format(qnt.quant(value, rettype='string', **self._str_quantization),
                                       unit, self.__class__.__name__)

    def get_str(self, unit=None, **vargsd):
        """Quantity.get_str()

        string representation

        >>> from EngineeringTools.quantities.quantitiesbase import *
        >>> from EngineeringTools.quantities.mechanics import *

        >>> k = Scalar(1.0); k.set_displayUnit('%')
        >>> print(k.get_str())
         100     %       (Scalar)
        >>> print(k.get_str(withQuantity=False))
         100     %      
        >>> print(k.get_str(withUnit=False))
         100    
        >>> print(k.get_str(alignment=False))
        100 % (Scalar)
        >>> print(k.get_str(withQuantity=False, alignment=False))
        100 %
        >>> print(k.get_str(withUnit=False, alignment=False))
        100
        >>> L = Distance(1.0, 'm')
        >>> print(L.get_str(unit='km'))
           0.001 km      (Distance)
        >>> print(L.get_str(unit='mm'))
        1000.000 mm      (Distance)
        """
        # logging.critical(f'{unit}, {vargsd}')
        if unit is None:
            unit = self._displayUnit
        value = self.convert2unit(self._value, unit)
        if self._str_quantization is None:
            ret = qnt.quant(value, rettype='string', **DEFAULT_STR_QUANTIZATION)
        else:
            ret = qnt.quant(value, rettype='string', **self._str_quantization)
        if not vargsd.get('alignment', True):
            ret = ret.strip() #IGNORE:E1103
        if vargsd.get('withUnit', True):
            if vargsd.get('alignment', True):
                ret = '%s %-7s' % (ret, unit)
                if vargsd.get('withQuantity', True):
                    ret = '%s (%s)' % (ret, self.__class__.__name__)
            else:
                ret = '%s %s' % (ret, unit)
                if vargsd.get('withQuantity', True):
                    ret = '%s (%s)' % (ret, self.__class__.__name__)
        return ret


    def __repr__(self):
        """string representation

        >>> from EngineeringTools.quantities.quantitiesbase import *
        >>> from EngineeringTools.quantities.mechanics import *

        >>> Quantity.set_displayUnitSystem('mechanicalEngineering')
        >>> L = Distance(1.2345678901234567890, 'mm')
        >>> print(L)
           1.235 mm (Distance)
        >>> print(repr(L))
        quantities.Distance(value=0.0012345678901234567, unit='m', displayUnit='mm')

        """
        return 'quantities.%s(value=%s, unit=%s, displayUnit=%s)' % (\
                self.__class__.__name__, \
                repr(self._value), \
                repr(self._isoUnit), \
                repr(self._displayUnit))


    def _repr_html_(self):
        html = f'<font face="monospace">{str(self).replace(" ","&nbsp;")}</font>\n'
        return html


    def __add__(self, obj):
        """add two equal quantities

            >>> from EngineeringTools.quantities.quantitiesbase import *
            >>> from EngineeringTools.quantities.mechanics import *

            >>> L1 = Distance(1.3, 'm', 'mm'); print(L1)
            1300.000 mm (Distance)
            >>> L2 = Distance(0.6, 'm', 'm'); print(L2)
               0.600 m (Distance)
            >>> L = L1 + L2; print (L)
            1900.000 mm (Distance)

            >>> A = Area(0.1, 'm^2'); print (A)
            100000     mm^2 (Area)
            >>> L + A  #doctest: +ELLIPSIS
            Traceback (most recent call last):
                ...
            EngineeringTools.quantities.quantitiesbase.ParaDInF_quantity_ErrorQuantitiesDoNotMatch:...
            >>> A + L  #doctest: +ELLIPSIS
            Traceback (most recent call last):
                ...
            EngineeringTools.quantities.quantitiesbase.ParaDInF_quantity_ErrorQuantitiesDoNotMatch:...
            >>> L + 7.0 #doctest: +ELLIPSIS
            Traceback (most recent call last):
                ...
            EngineeringTools.quantities.quantitiesbase.ParaDInF_quantity_ErrorQuantitiesDoNotMatch:...
            >>> 7.0 + L #doctest: +ELLIPSIS
            Traceback (most recent call last):
                ...
            TypeError: unsupported operand type(s) for +: 'float' and 'Distance'

        """
        if isinstance(obj, self.__class__):
            ret = self.__class__(self)
            ret._value += obj._value
        elif isinstance(obj, numbers.Real) and np.isnan(obj): # FIXIT: is that really working, shall ignore nan, e.g. for sum in pandas
            ret = self.__class__(self)
            self.log.info('ignoring add nan')
        else:
            raise ParaDInF_quantity_ErrorQuantitiesDoNotMatch("{} + {}  {}".format(self, obj, type(obj)))
        return ret

    def __sub__(self, obj):
        """add two equal quantities

            >>> from EngineeringTools.quantities.quantitiesbase import *
            >>> from EngineeringTools.quantities.mechanics import *
            >>> L1 = Distance(1.3, 'm', 'mm'); print(L1)
            1300.000 mm (Distance)
            >>> L2 = Distance(0.6, 'm', 'm'); print(L2)
               0.600 m (Distance)
            >>> L = L1 - L2; print(L)
             700.000 mm (Distance)

            >>> A = Area(0.1, 'm^2'); print(A)
            100000     mm^2 (Area)
            >>> L - A  #doctest: +ELLIPSIS
            Traceback (most recent call last):
                ...
            EngineeringTools.quantities.quantitiesbase.ParaDInF_quantity_ErrorQuantitiesDoNotMatch:...
            >>> A - L  #doctest: +ELLIPSIS
            Traceback (most recent call last):
                ...
            EngineeringTools.quantities.quantitiesbase.ParaDInF_quantity_ErrorQuantitiesDoNotMatch:...
            >>> L - 7.0  #doctest: +ELLIPSIS
            Traceback (most recent call last):
                ...
            EngineeringTools.quantities.quantitiesbase.ParaDInF_quantity_ErrorQuantitiesDoNotMatch:...
            >>> 7.0 - L  #doctest: +ELLIPSIS
            Traceback (most recent call last):
                ...
            TypeError: unsupported operand type(s) for -: 'float' and 'Distance'

        """
        if isinstance(obj, self.__class__):
            ret = self.__class__(self)
            ret._value -= obj._value
            return ret
        elif isinstance(obj, UVal):
            return self.uval - obj
        else:
            raise ParaDInF_quantity_ErrorQuantitiesDoNotMatch("{} - {}  {}".format(self, obj, type(obj)))


    def __neg__(self):
        ret = self.__class__(self)
        ret._value = -self._value
        return ret


    def __mul__(self, obj):
        """self * obj

            >>> from EngineeringTools.quantities.quantitiesbase import *
            >>> from EngineeringTools.quantities.mechanics import *
            >>> L1 = Distance(1.0, 'm')
            >>> print(L1 * 2.0)
            2000.000 mm (Distance)
            >>> print(L1 * 2)
            2000.000 mm (Distance)
            >>> print(L1 * L1)
            1.000 {m^2}
            >>> print(2.0 * L1)
            2000.000 mm (Distance)
            >>> L1 *= 2.0; print(L1)
            2000.000 mm (Distance)

        """
        if isinstance(obj, (int, float, numbers.Number)):
            ret = type(self)(self)
            ret._value *= obj
            return ret
        elif isinstance(obj, UVal):
            return UVal(self.uval) * UVal(obj)
        elif isinstance(obj, Quantity):
            return UVal(self.uval) * UVal(obj.uval)
        else:
            raise ParaDInF_quantity_ErrorQuantitiesDoNotMatch("{} * {}  {}".format(self, obj, type(obj)))

    __imul__ = __mul__

    def __rmul__(self, obj):
        return self.__mul__(obj)


    def __pow__(self, exp):
        """ self ** obj

        >>> from EngineeringTools.quantities.quantitiesbase import *
        >>> from EngineeringTools.quantities.mechanics import *
        >>> d1 = Distance(2.0, 'm')
        >>> d1**2
        UVal(4.0, {'meter': Fraction(2, 1)})

        >>> s1 = Scalar(2., '1')
        >>> d1 ** s1
        UVal(4.0, {'meter': Fraction(2, 1)})
        
        >>> d2 = Distance(4.0, 'm')
        >>> s2 = Scalar(0.5, '1')
        >>> d2 ** s2
        UVal(2.0, {'meter': Fraction(1, 2)})
        
        """
        if isinstance(self, QuantityNumeric):
            value = self.uval
        else:
            raise Exception("not supported")
        if isinstance(exp, (ETQ.Number, ETQ.Scalar)):
            exp = exp.get_value()

        if isinstance(exp, int):
            exp = float(exp)
    
        if isinstance(value, (float, int)) and isinstance(exp, float):
            return _np.power(value, exp)
        elif isinstance(value, UVal) and isinstance(exp, float):
            units = {k:v*exp for k,v in value._units.items()}
            return UVal(_np.power(value.get_value(), exp), units)
        else:
            raise ParaDInF_quantity_ErrorQuantitiesDoNotMatch('type not recognized: {}, {}'.format(type(value), type(exp)))


    def __truediv__(self, obj):
        """self / obj

            >>> from EngineeringTools.quantities.quantitiesbase import *
            >>> from EngineeringTools.quantities.mechanics import *

            >>> L1 = Distance(1.0, 'm')
            >>> print(L1 / 2.0)
             500.000 mm (Distance)
            >>> print(L1 / 2)
             500.000 mm (Distance)
            >>> print(L1 / L1)
            1.000 {}
            >>> print(2.0 / L1)
            2.000 {m^-1}
            >>> L1 /= 2.0; print(L1)
             500.000 mm (Distance)

        """
        if isinstance(obj, (int, float, numbers.Number)):
            ret = type(self)(self)
            ret._value /= obj
            return ret
        elif isinstance(obj, UVal):
            return self.uval / UVal(obj)
        elif isinstance(obj, Quantity):
            return self.uval / obj.uval
        else:
            raise ParaDInF_quantity_ErrorQuantitiesDoNotMatch('obj is of type: {}'.format(type(obj)))

    __div__ = __truediv__
    __idiv__ = __div__

    def __rdiv__(self, obj):
        """obj/self

            >>> from EngineeringTools.quantities.quantitiesbase import *
            >>> from EngineeringTools.quantities.mechanics import *
            >>> L1 = Distance(2.0, 'm')
            >>> print(1. / L1)
            0.5000 {m^-1}

        """
        if isinstance(obj, (int, float, numbers.Number)):
            return obj / self.uval
        elif isinstance(obj, UVal):
            return UVal(obj) / self.uval
        elif isinstance(obj, Quantity):
            return obj.uval / self.uval
        else:
            raise ParaDInF_quantity_ErrorQuantitiesDoNotMatch


    __rtruediv__ = __rdiv__


    def __cmp__(self, obj):
        """cmp ( )

            >>> from EngineeringTools.quantities.quantitiesbase import *
            >>> from EngineeringTools.quantities.mechanics import *

            >>> cmp = lambda x, y: (x > y) - (x < y)

            >>> L1 = Distance(1.0, 'm')
            >>> L2 = Distance(1.1, 'm')
            >>> print(cmp(L1, L2))
            -1
            >>> print(cmp(L2, L1))
            1
            >>> print(cmp(L1, L1))
            0
            >>> print(L1 > L2)
            False
            >>> print(L1 >= L2)
            False
            >>> print(L1 < L2)
            True
            >>> print(L1 <= L2)
            True
            >>> print(L1 == L2)
            False
            >>> print(L1 != L2)
            True
            >>> print(L1 == None)
            False
            >>> print(L1 != None)
            True
        """
        if isinstance(obj, self.__class__):
            cmp = lambda x, y: (x > y) - (x < y)  # http://python-future.org/compatible_idioms.html
            return cmp(self._value, obj._value)
        else:
            raise ParaDInF_quantity_ErrorQuantitiesDoNotMatch(
                    '%s :: %s' % (type(obj), type(self)))

    def __lt__(self, obj):
        if isinstance(obj, self.__class__):
            return self._value < obj._value
        else:
            raise ParaDInF_quantity_ErrorQuantitiesDoNotMatch(
                    '%s :: %s' % (type(obj), type(self)))

    def __le__(self, obj):
        if isinstance(obj, self.__class__):
            return self._value <= obj._value
        else:
            raise ParaDInF_quantity_ErrorQuantitiesDoNotMatch(
                    '%s :: %s' % (type(obj), type(self)))

    def __gt__(self, obj):
        if isinstance(obj, self.__class__):
            return self._value > obj._value
        else:
            raise ParaDInF_quantity_ErrorQuantitiesDoNotMatch(
                    '%s :: %s' % (type(obj), type(self)))

    def __ge__(self, obj):
        if isinstance(obj, self.__class__):
            return self._value >= obj._value
        else:
            raise ParaDInF_quantity_ErrorQuantitiesDoNotMatch(
                    '%s :: %s' % (type(obj), type(self)))

    def __eq__(self, obj):
        if obj is None:
            return False
        elif isinstance(obj, self.__class__):
            return self._value == obj._value
        else:
            raise ParaDInF_quantity_ErrorQuantitiesDoNotMatch(
                    '%s :: %s' % (type(obj), type(self)))

    def __ne__(self, obj):
        if obj is None:
            return True
        elif isinstance(obj, self.__class__):
            return self._value != obj._value
        else:
            raise ParaDInF_quantity_ErrorQuantitiesDoNotMatch(
                    '%s :: %s' % (type(obj), type(self)))



    def convert2iso(self, value, unit, typecast=False):
        """Quantity.convert2iso(value, unit)

        convert value from unit to iso-unit

        """
        try:
            return value * self._units[unit]
        except KeyError as reason:
            self.log.error('KeyError unit: %s; %s', self.get_quantity_name(), reason)
            raise reason


    def convert2unit(self, value, unit):
        """Quantity.convert2unit(value, unit)

        convert value from iso-unit to unit

        """
        try:
            return value / self._units[unit]
        except KeyError as reason:
            self.log.error('KeyError unit: %s; %s', self.get_quantity_name(), reason)
            raise reason

    @classmethod
    def get_units(cls):
        """Quantity.get_units()

        list of available units

        """
        return tuple(sorted(cls._units.keys()))

    list_units = get_units  # TODO: shall that stay?



    def get_unitsPreferred(self):
        """Quantity.get_unitsPreferred()

        list of preferred units

        """
        return tuple(self._unitsPreferred)



    def get_isoUnit(self):
        """Quantity.get_isoUnit()"""
        return self._isoUnit


    def get_displayUnit(self):
        """Quantity.get_displayUnit()"""
        return self._displayUnit


    def set_displayUnit(self, displayUnit=None):
        """Quantity.set_displayUnit(displayUnit)

        values for displayUnit:
        =======================
            - 'unit'
            - '__AUTO__'
            - '__ISO__'
            - '__unitSystem__'
            - None: automatic selection of displayUnit

        some examples:
        ==============

            >>> from EngineeringTools.quantities.quantitiesbase import *
            >>> from EngineeringTools.quantities.mechanics import *

            >>> q = Distance(0.0000001, 'm')
            >>> q.set_displayUnit('__AUTO__'); print(q)
               0.100 mu (Distance)
            >>> q = Distance(1000000.0, 'm')
            >>> q.set_displayUnit('__AUTO__'); print(q)
            1000.000 km (Distance)
            >>> q.set_displayUnit('__ISO__'); print(q)
            1000000.000 m (Distance)
            >>> Quantity.set_displayUnitSystem('mechanicalEngineering')
            >>> q.set_displayUnit('__unitSystem__'); print(q)
            1000000000.000 mm (Distance)

        @param displayUnit: displayUnit or method to choose displayUnit

        """
        if (displayUnit is None) and (self._displayUnitDefault is not None):
            displayUnit = self._displayUnitDefault
        if (displayUnit is None) or (displayUnit == '__unitSystem__'):
            t = self._displayUnitSystemList.get(Quantity._displayUnitSystem, None)
            if t:
                displayUnit = t.get('displayUnit', None)
            else:
                displayUnit = None
        if displayUnit is None:
            displayUnit = '__AUTO__'
        if displayUnit == '__AUTO__':
            if self._value == 0.0:
                t = self._displayUnitSystemList.get(Quantity._displayUnitSystem, None)
                if t:
                    displayUnit = t.get('displayUnit', None)
                else:
                    displayUnit = None
            else:
                vL = []
                for unit in self._unitsPreferred:
                    v = abs(self.convert2unit(self._value, unit))
                    if (v >= 0.05) and (v < 10000.0):
                        vL.append((abs(np.log10(v/100.0)-1), unit))
                vL.sort()
                if vL:
                    displayUnit = vL[0][1]
                else:
                    displayUnit = '__ISO__'
        if (displayUnit is None) or (displayUnit == '__ISO__'):
            displayUnit = self._isoUnit

        if displayUnit in self._units:
            self._displayUnit = displayUnit
            tmp = self._displayUnitSystemList.get(Quantity._displayUnitSystem, None)
            if tmp:
                self._str_quantization = tmp.get('str_quantization', None)
            else:
                self._str_quantization = None
        else:
            raise ParaDInF_quantity_ErrorUnitNotFound('unit "{:s}" is not available. Use: {}.'.format(displayUnit, ', '.join(self._units.keys())))
        # return self  # FIXME: better or not?


    def copy(self):
        """Quantity.copy()

        """
        import copy
        return copy.copy(self)


    def get_value(self, unit=None):
        """Quantity.get_value(unit=iso)

        get value in iso-unit od specified unit

        """
        if unit is None:
            return self._value
        else:
            if list(self._units).count(unit) < 1:
                raise AssertionError('unit "{}" is not available. Use: {}.'.format(unit, ', '.join(self._units.keys())))
            return self.convert2unit(self._value, unit)
    value = property(fget=get_value)

    def get_uval(self):
        """Quantity.get_uval()

        get value as UVal to do calculations with check of units

        """
        return UVal(self._value, self._uval_units)
    uval = property(fget=get_uval)



    def set_value(self, value, unit=''):
        """Quantity.setValue(value, unit=iso)

        value is converted from unit to iso-unit
        if no unit is specified, unit=isoUnit is assumed

        """
        if unit == '':
            unit = self._isoUnit
        if list(self._units).count(unit) < 1:
            raise ParaDInF_quantity_ErrorUnitNotFound('unit "%s" is not available' % unit)
        self._value = self.convert2iso(value, unit)


    def get_quantity_name(self):
        return self.__class__.__name__


    def get_as_dict(self, unit=None):
        """Quantity.get_as_dict()

        return quantity as dict

        """
        q = {}
        q['quantity'] = self.__class__.__name__
        if unit is None:
            unit = self._isoUnit
        q['value'] = self.convert2unit(self._value, unit)
        q['unit'] = unit
        return q


    def match_quantities(self, other):
        """does this quantities match?

        >>> from EngineeringTools.quantities.quantitiesbase import *
        >>> from EngineeringTools.quantities.mechanics import *

        >>> L = Distance(1.2, 'mm')
        >>> L2 = Distance(21231.2, 'km')
        >>> A = Area(1.1, 'mm^2')
        >>> L.match_quantities(L2)
        True
        >>> L.match_quantities(A)
        False
        """
        return type(other) is type(self)


    def check_match_quantities(self, other):
        """check whether this quantities match? raise an Exception ParaDInF_quantity_ErrorQuantitiesDoNotMatch

        >>> from EngineeringTools.quantities.quantitiesbase import *
        >>> from EngineeringTools.quantities.mechanics import *

        >>> L = Distance(1.2, 'mm')
        >>> L2 = Distance(21231.2, 'km')
        >>> A = Area(1.1, 'mm^2')
        >>> L.check_match_quantities(L2)
        >>> L.check_match_quantities(A)  #doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        EngineeringTools.quantities.quantitiesbase.ParaDInF_quantity_ErrorQuantitiesDoNotMatch:...
        """
        if not self.match_quantities(other):
            raise ParaDInF_quantity_ErrorQuantitiesDoNotMatch('quantities do not match: %s != %s' %
                                                                (other.__class__.__name__, self.__class__.__name__))


    def set_properties_from(self, obj):
        if isinstance(obj, self.__class__):
            self.set_displayUnit(obj.get_displayUnit())
        else:
            raise ParaDInF_quantity_ErrorQuantitiesDoNotMatch(
                    '%s :: %s' % (type(obj), type(self)))


    def abs(self):
        obj = self.copy()
        obj._value = np.abs(obj._value)
        return obj


################################################################################
class QuantityNumeric(Quantity):
    """base class for all numeric type quantities """

################################################################################
class QuantityDecimal(QuantityNumeric):
    """Quantity__dezimal base class

    base class for decimal values, now implemented as floating point values
    future improvements: from decimal import Decimal ...

    """

    def convert2iso(self, value, unit, typecast=False):
        """Quantity.convert2iso(value, unit)

        convert value from unit to iso-unit

        """
        if  typecast:
            value = float(value)
        else:
            assert isinstance(value, float), 'value must be a float'
        try:
            return value * self._units[unit]
        except KeyError as reason:
            self.log.error('KeyError unit: %s; %s', self.get_quantity_name(), reason)
            raise reason


    def convert2unit(self, value, unit):
        """Quantity.convert2unit(value, unit)

        convert value from iso-unit to unit

        """
        assert isinstance(value, float), 'value must be a float'
        try:
            return value / self._units[unit]
        except KeyError as reason:
            self.log.error('KeyError unit: %s; %s', self.get_quantity_name(), reason)
            raise reason


    def __eq__(self, obj):
        if obj is None:
            return False
        elif isinstance(obj, self.__class__):
            return _float_equal(self._value, obj._value)
        else:
            raise ParaDInF_quantity_ErrorQuantitiesDoNotMatch('%s :: %s' % (type(obj), type(self)))

    def __ne__(self, obj):
        if obj is None:
            return True
        elif isinstance(obj, self.__class__):
            return not _float_equal(self._value, obj._value)
        else:
            raise ParaDInF_quantity_ErrorQuantitiesDoNotMatch('%s :: %s' % (type(obj), type(self)))


    def quant(self, method='1', precision=0, unit=None):
        """quantisize value

        >>> from EngineeringTools.quantities.quantitiesbase import *
        >>> from EngineeringTools.quantities.mechanics import *

        >>> d = Distance(12345.678901234, 'm'); d.quant(); print(d.get_value('m'))
        12346.0
        >>> d = Distance(12345.678901234, 'm'); d.quant('R10+'); print(d.get_value('m'))
        12500.0
        >>> d = Distance(12345.678901234, 'm'); d.quant('1', 2); print(d.get_value('m'))
        12345.68
        >>> d = Distance(12345.678901234, 'm'); d.quant('1', 2, unit='km'); print(d.get_value('m'))
        12350.0
        """
        if unit is None:
            unit = self._isoUnit
        value = self.get_value(unit)
        value = qnt.quant(value, method=method, precision=precision)
        self.set_value(value, unit)




################################################################################
class QuantityFloat(QuantityNumeric):
    """QuantityFloat base class

    base class for floating point values

    """

    def convert2iso(self, value, unit, typecast=False):
        """Quantity.convert2iso(value, unit) ... convert value from unit to iso-unit"""
        if  typecast:
            value = float(value)
        else:
            assert isinstance(value, float), 'value must be a float'
        try:
            return value * self._units[unit]
        except KeyError as reason:
            self.log.error('KeyError unit: %s; %s', self.get_quantity_name(), reason)
            raise reason


    def convert2unit(self, value, unit):
        """Quantity.convert2unit(value, unit) ... convert value from iso-unit to unit"""
        assert isinstance(value, float), 'value must be a float'
        try:
            return value / self._units[unit]
        except KeyError as reason:
            self.log.error('KeyError unit: %s; %s', self.get_quantity_name(), reason)
            raise reason


    def __eq__(self, obj):
        if obj is None:
            return False
        elif isinstance(obj, self.__class__):
            return _float_equal(self._value, obj._value)
        else:
            raise ParaDInF_quantity_ErrorQuantitiesDoNotMatch('%s :: %s' % (type(obj), type(self)))

    def __ne__(self, obj):
        if obj is None:
            return True
        elif isinstance(obj, self.__class__):
            return not _float_equal(self._value, obj._value)
        else:
            raise ParaDInF_quantity_ErrorQuantitiesDoNotMatch('%s :: %s' % (type(obj), type(self)))


    def quant(self, method='1', precision=0, unit=None):
        """quantize value

        >>> from EngineeringTools.quantities.quantitiesbase import *
        >>> from EngineeringTools.quantities.mechanics import *

        >>> d = Force(12345.678901234, 'N'); d.quant(); print(d.get_value('N'))
        12346.0
        >>> d = Force(12345.678901234, 'N'); d.quant('R10+'); print(d.get_value('N'))
        12500.0
        >>> d = Force(12345.678901234, 'N'); d.quant('1', 2); print(d.get_value('N'))
        12345.68
        >>> d = Force(12345.678901234, 'N'); d.quant('1', 2, unit='kN'); print(d.get_value('N'))
        12350.0
        """
        if unit is None:
            unit = self._isoUnit
        value = self.get_value(unit)
        value = qnt.quant(value, method=method, precision=precision)
        self.set_value(value, unit)


    def sign(self):
        """
        >>> from EngineeringTools.quantities.quantitiesbase import *
        >>> from EngineeringTools.quantities.mechanics import *

        >>> d = Force(123, 'N');
        >>> d.sign()
        1.0
        
        >>> d = Force(-123, 'N');
        >>> d.sign()
        -1.0
        
        """
        return np.sign(self.get_value())


    def abs(self):
        """
        >>> from EngineeringTools.quantities.quantitiesbase import *
        >>> from EngineeringTools.quantities.mechanics import *

        >>> d = Force(123, 'N');
        >>> d.abs()
        quantities.Force(value=123.0, unit='N', displayUnit='kN')
        
        >>> d = Force(-123, 'N');
        >>> d.abs()
        quantities.Force(value=123.0, unit='N', displayUnit='kN')
        
        """        
        x = self.copy()
        x.set_value(np.abs(x.get_value()))
        return x    
    


###############################################################################
class QuantityFloatOffset(QuantityFloat):
    """Quantity  floating point with offset"""
    _isoUnit = '1'
    _units = {'1':(1.0, 0.0)}

    def convert2iso(self, value, unit, typecast=False):
        """Quantity.convert2iso(value, unit) ... convert value from unit to iso-unit"""
        if  typecast:
            value = float(value)
        else:
            assert isinstance(value, float), 'value must be a float'
        try:
            return value * self._units[unit][0] + self._units[unit][1]
        except KeyError as reason:
            self.log.error('KeyError unit: %s; %s', self.get_quantity_name(), reason)
            raise reason


    def convert2unit(self, value, unit):
        """Quantity.convert2unit(value, unit) ... convert value from iso-unit to unit"""
        assert isinstance(value, float), 'value must be a float'
        try:
            return value / self._units[unit][0] - self._units[unit][1]
        except KeyError as reason:
            self.log.error('KeyError unit: %s; %s', self.get_quantity_name(), reason)
            raise reason



###############################################################################
class QuantityInt(QuantityNumeric):
    """Quantity  integer"""
    _isoUnit = '1'
    _units = {'1':1}

    def convert2iso(self, value, unit, typecast=False):
        """QuantityInt.convert2iso(value, unit) ... convert value from unit to iso-unit"""
        if  typecast:
            value = int(value)
        else:
            assert isinstance(value, int), 'value must be a int'
        try:
            return value * self._units[unit]
        except KeyError as reason:
            self.log.error('KeyError unit: %s; %s', self.get_quantity_name(), reason)
            raise reason


    def convert2unit(self, value, unit):
        """QuantityInt.convert2unit(value, unit) ... convert value from iso-unit to unit"""
        assert isinstance(value, int), 'value must be a int'
        try:
            return value / self._units[unit]
        except KeyError as reason:
            self.log.error('KeyError unit: %s; %s', self.get_quantity_name(), reason)
            raise reason


    #def __str__(self):
    #    """QuantityInt.__str__() ... string representation"""
    #    return '%d {%s}' % (self.convert2unit(self._value, self._displayUnit), self._displayUnit)

    #__repr__ = __str__


################################################################################
class QuantityString(Quantity):
    """Quantity  string

    >>> from EngineeringTools.quantities.quantitiesbase import *
    >>> from EngineeringTools.quantities.mechanics import *
    >>> cmp = lambda x, y: (x > y) - (x < y)

    >>> s1 = Text('test')
    >>> s2 = Text('test')
    >>> print(s1)
    test (Text)
    >>> print(repr(s1))
    quantities.Text(value='test')
    >>> s3 = s1 + 'abc'; print(s3)
    testabc (Text)
    >>> print('abc' + s1)
    abctest (Text)
    >>> print(s1 == s2)
    True
    >>> print(s1 == s3)
    False
    >>> print(s1 > s3)
    False
    >>> print(cmp(s1, s3))
    -1

    """
    _isoUnit = ''
    _units = {' ':0, '':0, 'str':0}

    def __init__(self, value, unit=None, displayUnit=None, typecast=False):
        if unit is None and not isinstance(value, (Quantity, UVal)):
            unit = self._isoUnit
        Quantity.__init__(self, value, unit=unit, displayUnit=displayUnit, typecast=typecast)

    def convert2iso(self, value, unit, typecast=False):
        """Quantity.convert2iso(value, unit) ... convert value from unit to iso-unit"""
        if  typecast:
            value = str(value)
        else:
            assert isinstance(value, str), 'value must be a string'
        return value

    def convert2unit(self, value, unit):
        """Quantity.convert2unit(value, unit) ... convert value from iso-unit to unit"""
        assert isinstance(value, str), 'value must be a string'
        return value

    def set_displayUnit(self, displayUnit=None):
        """Quantity.set_displayUnit(displayUnit)"""
        if (displayUnit is None) or (displayUnit == '__unitSystem__') or \
           (displayUnit == '__AUTO__') or (displayUnit == '__ISO__'):
            displayUnit = ''
        if displayUnit in self._units:
            self._displayUnit = displayUnit
        else:
            raise ParaDInF_quantity_ErrorUnitNotFound('unit "%s" is not available' % displayUnit)


    def __str__(self, unit=None):
        """Quantity.__str__() ... string representation"""
        return '%s (%s)' % (self._value, self.__class__.__name__)


    def get_str(self, unit=None, **vargsd):
        """Quantity.get_str()

        string representation

        """
        ret = str(self._value)
        if vargsd.get('withUnit', True):
            ret = '%s (%s)' % (ret, self.__class__.__name__)
        return ret


    def __repr__(self):
        return 'quantities.%s(value=%s)' % (self.__class__.__name__, repr(self._value))

    def __add__(self, obj):
        """add two strings """
        if isinstance(obj, self.__class__):
            ret = self.__class__(self)
            ret._value += obj._value
        elif isinstance(obj, str):
            ret = self.__class__(self)
            ret._value += obj
        else:
            raise ParaDInF_quantity_ErrorQuantitiesDoNotMatch
        return ret

    def __radd__(self, obj):
        """add two strings """
        if isinstance(obj, str):
            ret = self.__class__(self)
            ret._value = obj + ret._value
        else:
            raise ParaDInF_quantity_ErrorQuantitiesDoNotMatch
        return ret

    def __mul__(self, obj):
        raise NotImplementedError('makes no sense')
    def __imul__(self, obj):
        raise NotImplementedError('makes no sense')
    def __rmul__(self, obj):
        raise NotImplementedError('makes no sense')
    def __truediv__(self, obj):
        raise NotImplementedError('makes no sense')
    def __div__(self, obj):
        raise NotImplementedError('makes no sense')
    def __idiv__(self, obj):
        raise NotImplementedError('makes no sense')


###############################################################################
class QuantityBoolean(Quantity):
    """Quantity  boolean
     """
    _isoUnit = 'boolean'
    _units = {'boolean':{True:True, False:False},
              'T/F':{True:'T', False:'F'},
              'True/False':{True:'True', False:'False'},
              '1/0':{True:1, False:0}}


    def __init__(self, value, unit=None, displayUnit=None, typecast=False):
        if unit is None and not isinstance(value, (Quantity, UVal)):
            unit = self._isoUnit
        Quantity.__init__(self, value, unit=unit, displayUnit=displayUnit, typecast=typecast)

    def __str__(self, unit=None):
        """Quantity.__str__()

        string representation

        """
        if unit is None:
            unit = self._displayUnit
        value = self.convert2unit(self._value, unit)
        return '%8s (%s)' % (value, self.__class__.__name__)

    def get_str(self, unit=None, **vargsd):
        """Quantity.get_str()

        string representation

        """
        if unit is None:
            unit = self._displayUnit
        value = self.convert2unit(self._value, unit)
        ret = '%10s' % value
        if not vargsd.get('alignment', True):
            ret = ret.strip() #IGNORE:E1103
        if vargsd.get('withUnit', True):
            if vargsd.get('alignment', True):
                if vargsd.get('withQuantity', True):
                    ret = '%s (%s)' % (ret, self.__class__.__name__)
            else:
                if vargsd.get('withQuantity', True):
                    ret = '%s(%s)' % (ret, self.__class__.__name__)
        return ret


    def convert2iso(self, value, unit, typecast=False):
        """convert2iso(value, unit) ... convert value from unit to iso-unit"""
        if  typecast:
            raise NotImplementedError()
        else:
            if not isinstance(value, (bool, str)):
                raise AssertionError('value must be a bool or str')
        try:
            dur = {}
            for k, v in self._units[unit].items():
                if isinstance(v, str):
                    v = v.upper()
                dur[v] = k
            if isinstance(value, str):
                value = value.upper()
            return dur[value]
        except KeyError as reason:
            self.log.error('KeyError unit: %s; %s', self.get_quantity_name(), reason)
            raise reason


    def convert2unit(self, value, unit):
        """convert2unit(value, unit) ... convert value from iso-unit to unit"""
        assert isinstance(value, bool), 'value must be a bool'
        try:
            return self._units[unit][value]
        except KeyError as reason:
            self.log.error('KeyError unit: %s; %s', self.get_quantity_name(), reason)
            raise reason

    def set_displayUnit(self, displayUnit=None):
        """Quantity.set_displayUnit(displayUnit)"""
        if (displayUnit is None) or (displayUnit == '__unitSystem__') or \
           (displayUnit == '__AUTO__') or (displayUnit == '__ISO__'):
            displayUnit = self._isoUnit
        if displayUnit in self._units:
            self._displayUnit = displayUnit
        else:
            raise ParaDInF_quantity_ErrorUnitNotFound('unit "%s" is not available' % displayUnit)


    def __add__(self, obj):
        raise NotImplementedError('makes no sense')
    def __sub__(self, obj):
        raise NotImplementedError('makes no sense')
    def __mul__(self, obj):
        raise NotImplementedError('makes no sense')
    def __imul__(self, obj):
        raise NotImplementedError('makes no sense')
    def __rmul__(self, obj):
        raise NotImplementedError('makes no sense')
    def __truediv__(self, obj):
        raise NotImplementedError('makes no sense')
    def __div__(self, obj):
        raise NotImplementedError('makes no sense')
    def __idiv__(self, obj):
        raise NotImplementedError('makes no sense')
    def __lt__(self, obj):
        raise NotImplementedError('makes no sense')
    def __le__(self, obj):
        raise NotImplementedError('makes no sense')
    def __gt__(self, obj):
        raise NotImplementedError('makes no sense')
    def __ge__(self, obj):
        raise NotImplementedError('makes no sense')

#eof

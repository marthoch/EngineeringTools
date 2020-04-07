#!/usr/bin/env python3
# pylint: disable=line-too-long,no-else-return,missing-function-docstring,missing-class-docstring,empty-docstring
"""do calculation with check of units

"""
__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"

# run doctest, workaround relative import
if __name__ == '__main__':
    import sys
    import doctest # pylint: disable=import-outside-toplevel
    import EngineeringTools.quantities as ETQ             # pylint: disable=import-self
    ETQ.Quantity.set_displayUnitSystem('mechanicalEngineering')
    module_name = 'EngineeringTools.uval'      # pylint: disable=invalid-name
    module = __import__(module_name, fromlist=['*'], level=0)  # pylint: disable=invalid-name
    print(doctest.testmod(module, optionflags=doctest.ELLIPSIS))
    sys.exit()

# $Source$

from fractions import Fraction
from . import qnt
from .quantities import quantitiesbase as base


class EngineeringTools_uval_Error(Exception):
    """Exception: uval """


class UVal:
    """ class to do calculation with check of units

        >>> L1 = UVal(12.3, {'meter':1})
        >>> L2 = UVal(4.56, {'meter':1})
        >>> T1 = UVal(2.34, {'second':1})
        >>> v  = UVal(11.1, {'meter':1, 'second':-1})

        >>> print(L1)
        12.30 {m}
        >>> print(L1 + L2)
        16.86 {m}
        >>> print(L1 / L2)
        2.697 {}
        >>> print(L1 / T1)
        5.256 {m s^-1}
        >>> print(L1 + T1)
        Traceback (most recent call last):
        ...
        EngineeringTools.uval.EngineeringTools_uval_Error: units do not match: {'meter': Fraction(1, 1)} != {'second': Fraction(1, 1)}
        >>> print(L1 / T1 + v)
        16.36 {m s^-1}

    """

    #__slots__ = ('si_base_units', '_si_base_units_list', '_value', '_units')

    si_base_units = {'meter':'m', 'kilogram':'kg', 'second':'s',
                     'ampere':'A', 'kelvin':'K', 'mole':'mol', 'candela':'cd'}
    _si_base_units_list = ['kilogram', 'meter', 'second',
                           'kelvin', 'ampere', 'mole', 'candela']  # order is essential!


    @classmethod
    def add_base_unit(cls, unit, abriviation):
        cls.si_base_units[unit] = abriviation
        if unit not in cls._si_base_units_list:
            cls._si_base_units_list.append(unit)


    def __init__(self, value, units=None):
        """ UVal(value, units)

            >>> UVal(123.1, {'meter':1, 'kilogram':1, 'second':-2})           # = 123.1 N
            UVal(123.1, {'kilogram': Fraction(1, 1), 'meter': Fraction(1, 1), 'second': Fraction(-2, 1)})

            >>> print(UVal(123.1, {'meter':1, 'kilogram':1, 'second':-2}))     # = 123.1 N
            123.1 {kg m s^-2}

            >>> print(UVal(123.1, {'meter':Fraction(1,2)}))          # = 123.1 sqrt(meter)
            123.1 {m^1/2}


        @param value: in iso units
        @type  value: float, int, ...

        @param units:
        @type  units: dict {baseunit:exp, ...}
            baseunit:  iso base units: ['meter', 'kilogram', 'second', 'ampere', 'kelvin', 'mole', 'candela']
            exp:       int, tuple (1, 3) = 1/3 or Fraction

        """

        if isinstance(value, UVal):
            self._value, self._units = value._value, dict(value._units)
            # no copy, deep copy ...?
        else:
            if units is None:
                self._value = value
                self._units = {}
            elif isinstance(units, dict):
                self._value = value
                self._units = {}
                for unitname in units:
                    self._units[unitname] = Fraction(units[unitname])
                    if self._units[unitname] == 0:
                        self._units.pop(unitname)
            else:
                raise EngineeringTools_uval_Error('units must be not None')


    def __str__(self):
        unitstr = '{'
        for unitname in self._si_base_units_list:
            if unitname in  self._units:
                pot = self._units[unitname]
                if pot != 0:
                    unitstr += self.si_base_units[unitname]
                    if pot != 1:
                        unitstr += '^%s' % pot
                    unitstr += ' '
        if unitstr[-1] == ' ':
            unitstr = unitstr[:-1] + '}'
        else:
            unitstr = unitstr + '}'
        return '{:#.4g} {}'.format(qnt.quant(self._value, method='1r', precision=4), unitstr)


    def _repr_units(self, units=None):
        unitstr = '{'
        if units is None:
            units = self._units
        for unitname in self._si_base_units_list:
            if unitname in units:
                if units[unitname] != 0:
                    unitstr += "{!r}: {!r}, ".format(unitname, units[unitname])
        if unitstr.endswith(', '):
            unitstr = unitstr[:-2] + '}'
        else:
            unitstr = unitstr + '}'
        return unitstr


    def __repr__(self):
        unitstr = self._repr_units()
        return 'UVal(%s, %s)' % (repr(self._value), unitstr)


    def _repr_html_(self):
        html = """<font face="monospace">{}</font>\n""".format(str(self))
        return html


    def __neg__(self):
        """
        >>> v = UVal(1.1, {})
        >>> print(-v)
        -1.100 {}

        """
        val = UVal(self)
        val._value *= -1
        return val


    def __abs__(self):
        """
        >>> print(abs(UVal(-1.1, {})))
        1.100 {}
        >>> print(abs(UVal(1.1, {})))
        1.100 {}

        """
        val = UVal(self)
        val._value = abs(val._value)
        return val


    def __add__(self, obj):
        """
        >>> print(UVal(1.0, {}) + 10.0)
        11.00 {}
        >>> print(1.0 + UVal(1.0, {}))
        2.000 {}

        """
        if isinstance(obj, float):
            self.check_units({})
            obj = UVal(obj, {})
        if not isinstance(obj, UVal):
            raise EngineeringTools_uval_Error('wrong type: %s + %s' % (self, obj))
        self.check_units(obj._units)
        return UVal(self._value + obj._value, self._units)


    def __radd__(self, obj):
        return UVal(self + obj)


    def __sub__(self, obj):
        if isinstance(obj, UVal):
            pass
        elif isinstance(obj, float):
            obj = UVal(obj, {})
        elif isinstance(obj, base.Quantity):
            obj = obj.uval
        else:
            raise EngineeringTools_uval_Error('wrong type: %s - %s' % (self, obj))
        self.check_units(obj._units)
        return UVal(self._value - obj._value, self._units)


    __isub__ = __sub__


    def __rsub__(self, obj):
        return UVal(-self + obj)


    def __mul__(self, obj):
        """
        >>> print(UVal(1.0, {}) * UVal(2.0, {}))
        2.000 {}
        >>> print(1.0 * UVal(2.0, {}))
        2.000 {}
        """
        if isinstance(obj, base.Quantity):
            obj = obj.uval
        if isinstance(obj, UVal):
            newunits = {}
            for unitname in self._units:
                newunits[unitname] = self._units[unitname]
            for unitname in obj._units:
                newunits[unitname] = newunits.get(unitname, Fraction(0)) + obj._units[unitname]
            return UVal(self._value * obj._value, newunits)
        elif isinstance(obj, (float, int, )):
            return UVal(self._value * obj, self._units)
        else:
            raise EngineeringTools_uval_Error('wrong type: %s * %s' % (self, obj))


    def __rmul__(self, obj):
        if isinstance(obj, (float, int, )):
            return UVal(self._value * obj, self._units)
        else:
            raise EngineeringTools_uval_Error('wrong type: %s * %s' % (self, obj))


    def __div__(self, obj):
        """
        >>> print(UVal(1.0, {}) / UVal(2.0, {}))
        0.5000 {}
        >>> print(UVal(1.0, {}) / 2.0)
        0.5000 {}
        """
        if isinstance(obj, UVal):
            newunits = dict(self._units)
            for unitname in obj._units:
                newunits[unitname] = newunits.get(unitname, Fraction(0)) - obj._units[unitname]
            return UVal(self._value / float(obj._value), newunits)
        elif isinstance(obj, (float, int)):
            return UVal(self._value / float(obj), self._units)
        elif isinstance(obj, base.Quantity):
            return self / obj.uval
        else:
            raise EngineeringTools_uval_Error('wrong type: %s / %s' % (self, obj))


    __truediv__ = __div__


    def __rdiv__(self, obj):
        if isinstance(obj, (float, int)):
            newunits = dict(self._units)
            for unitname in newunits:
                newunits[unitname] *= -1
            return UVal(float(obj) / self._value , newunits)
        else:
            raise EngineeringTools_uval_Error('wrong type: %s / %s' % (obj, self))

    __rtruediv__ = __rdiv__


    def __pow__(self, obj):
        if isinstance(obj, int):
            expon = obj
        elif isinstance(obj, tuple):
            obj = Fraction(*obj)
            expon = float(obj.numerator) / float(obj.denominator)
        elif isinstance(obj, Fraction):
            obj = Fraction(obj)
            expon = float(obj.numerator) / float(obj.denominator)
        else:
            raise EngineeringTools_uval_Error('wrong type right value: %s ** %s' % (self, obj))
        newunits = dict(self._units)
        for unitname in newunits:
            newunits[unitname] *= obj
        return UVal(self._value ** expon, newunits)

    def __xor__(self, obj):  # IGNORE:R0201
        raise EngineeringTools_uval_Error('do not use ^: pow: ** ')
    def __rxor__(self, obj): # IGNORE:R0201
        raise EngineeringTools_uval_Error('do not use ^: pow: ** ')
    def __ixor__(self, obj): # IGNORE:R0201
        raise EngineeringTools_uval_Error('do not use ^: pow: ** ')


    def __cmp__(self, obj):
        """cmp ( )

            >>> cmp = lambda x, y: (x > y) - (x < y)
            >>> U1 = UVal(1.0, {'meter':1})
            >>> U2 = UVal(2.0, {'meter':1})
            >>> U3 = UVal(1.0, {})
            >>> print(cmp(U1, U2))
            -1
            >>> print(cmp(U2, U1))
            1
            >>> print(cmp(U1, U1))
            0
            >>> print(U1 > U2)
            False
            >>> print(U1 >= U2)
            False
            >>> print(U1 < U2)
            True
            >>> print(U1 <= U2)
            True
            >>> print(U1 == U2)
            False
            >>> print(U1 != U2)
            True
            >>> print(U1 == None)
            False
            >>> print(U1 != None)
            True
            >>> print(U1 != U3)
            Traceback (most recent call last):
            ...
            EngineeringTools.uval.EngineeringTools_uval_Error: units do not match: {'meter': Fraction(1, 1)} != {}
            >>> print(cmp(U1, 0))
            Traceback (most recent call last):
            ...
            EngineeringTools.uval.EngineeringTools_uval_Error: units do not match
            >>> print(U1 < 0.0)
            Traceback (most recent call last):
            ...
            EngineeringTools.uval.EngineeringTools_uval_Error: units do not match
            >>> print(U1 == 0.0)
            Traceback (most recent call last):
            ...
            EngineeringTools.uval.EngineeringTools_uval_Error: units do not match

        """
        if isinstance(obj, self.__class__):
            self.check_units(obj._units)
            cmp = lambda x, y: (x > y) - (x < y)
            return cmp(self._value, obj._value)
        else:
            raise EngineeringTools_uval_Error('units do not match')


    def __lt__(self, obj):
        if isinstance(obj, self.__class__):
            self.check_units(obj._units)
            return self._value < obj._value
        else:
            raise EngineeringTools_uval_Error('units do not match')


    def __le__(self, obj):
        if isinstance(obj, self.__class__):
            self.check_units(obj._units)
            return self._value <= obj._value
        else:
            raise EngineeringTools_uval_Error('units do not match')


    def __gt__(self, obj):
        if isinstance(obj, self.__class__):
            self.check_units(obj._units)
            return self._value > obj._value
        else:
            raise EngineeringTools_uval_Error('units do not match')


    def __ge__(self, obj):
        if isinstance(obj, self.__class__):
            self.check_units(obj._units)
            return self._value >= obj._value
        else:
            raise EngineeringTools_uval_Error('units do not match')


    def __eq__(self, obj):
        if obj is None:
            return False
        if isinstance(obj, self.__class__):
            self.check_units(obj._units)
            return self._value == obj._value
        else:
            raise EngineeringTools_uval_Error('units do not match')


    def __ne__(self, obj):
        if obj is None:
            return True
        if isinstance(obj, self.__class__):
            self.check_units(obj._units)
            return self._value != obj._value
        else:
            raise EngineeringTools_uval_Error('units do not match')


    def get_value(self):
        """returns the value as float, int, ...   """
        return self._value


    value = property(fget=get_value)


    def get_uval_units(self):
        """return units of UVal

        >>> F = UVal(123.1, {'meter':1, 'kilogram':1, 'second':-2})           # = 123.1 N
        >>> F.get_uval_units() == {'second': Fraction(-2), 'kilogram': Fraction(1), 'meter': Fraction(1)}
        True

        """
        units = {}
        for unitname in self._units.keys():
            if self._units[unitname] != 0:
                units[unitname] = self._units[unitname]
        return units


    def check_units(self, units):
        """compare units of UVal with units

            >>> F = UVal(123.1, {'meter':1, 'kilogram':1, 'second':-2})   # = 123.1 N
            >>> F.check_units({'meter':1, 'kilogram':1, 'second':-2})
            >>> F.check_units({'meter':0, 'kilogram':1, 'second':-2})
            Traceback (most recent call last):
            ...
            EngineeringTools.uval.EngineeringTools_uval_Error: units do not match: {'kilogram': Fraction(1, 1), 'meter': Fraction(1, 1), 'second': Fraction(-2, 1)} != {'kilogram': 1, 'second': -2}
            >>> F.check_units(F.get_uval_units())
            >>> F.check_units(F)

        @param units: Units to compare
        @type  units: dict, UVal

        """
        if isinstance(units, UVal):
            units = units._units # pylint: disable=protected-access
        for unitname in frozenset(list(self._units) + list(units)):
            if units.get(unitname, 0) != self._units.get(unitname, 0):
                raise EngineeringTools_uval_Error('units do not match: %s != %s' % (self._repr_units(), self._repr_units(units)))



    def quant(self, method='1r', precision=3):
        """quantize UVal

        retuns a quantized UVal. The object itself is not altered.

        see also paradinf.qnt.quant(...)

        >>> L = UVal(123.456, {'meter':1})
        >>> print(L)
        123.5 {m}
        >>> print(L.quant())
        123.0 {m}

        >>> L = UVal(173.456, {'meter':1})
        >>> print(L.quant('R5'))
        160.0 {m}
        >>> L = UVal(123.423, {'meter':1})
        >>> print(L.quant('2.5', 2))
        123.4 {m}

        """
        val = UVal(self)
        val._value = qnt.quant(val._value, method=method, precision=precision) # pylint: disable=protected-access
        return val



# test -------------------------------------------------------------------
def _test():
    """run doctest"""
    import doctest  # pylint: disable=wrong-import-position
    doctest.testmod()


# main -------------------------------------------------------------------
if __name__ == '__main__':
    #from paradinf import loggingconf
    #loggingconf.loggingconf()

    _test()

# eof --------------------------------------------------------------------

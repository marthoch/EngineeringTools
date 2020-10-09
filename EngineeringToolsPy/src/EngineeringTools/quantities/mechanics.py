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


# run doctest, workaround relative import
if __name__ == '__main__':
    import sys
    import doctest # pylint: disable=import-outside-toplevel
    from EngineeringTools import quantities as ETQ             # pylint: disable=reimported,import-outside-toplevel
    ETQ.Quantity.set_displayUnitSystem('mechanicalEngineering')
    module_name = 'EngineeringTools.quantities.mechanics'      # pylint: disable=invalid-name
    module = __import__(module_name, fromlist=['*'], level=0)  # pylint: disable=invalid-name
    module._setup_doctest()                                    # pylint: disable=protected-access
    print(doctest.testmod(module, optionflags=doctest.ELLIPSIS))
    sys.exit()

import math
import scipy.constants
from .quantitiesbase import Quantity, QuantityFloat, QuantityFloatOffset, QuantityInt, QuantityDecimal, QuantityBoolean, QuantityString, ParaDInF_quantity_Error, ParaDInF_quantity_ErrorQuantitiesDoNotMatch
from ..uval import UVal, EngineeringTools_uval_Error

################################################################################
#  classes quantities
################################################################################
class Acceleration(QuantityFloat):
    """Quantity  acceleration

    >>> a = Acceleration(1.0, 'g')
    >>> print(a.get_value('m/sec^2'))
    9.8...
    """
    _isoUnit = 'm/s2'
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'m/sec^2',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}
    _units = {'m/s2':1.0, 'm/sec^2':1.0, 'g':scipy.constants.g}
    _uval_units = {'meter':1, 'second':-2}

################################################################################
class Angle(QuantityDecimal):
    """Quantity  angle"""
    _isoUnit = 'rad'
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'deg',
                                                       'str_quantization':{'method':'1', 'precision':3}}}
    _units = {'rad':1.0, 'deg':math.pi/180, 'rot':2*math.pi}
    _uval_units = {}


###############################################################################
class Area(QuantityFloat):
    """Quantity  area"""
    _isoUnit = 'm2'
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'mm^2',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}
    _units = {'m2':1.0, 'm^2':1.0, 'mm2':1.0e-6, 'mm^2':1.0e-6, 'cm2':1.0e-4, 'cm^2':1.0e-4, 'dm2':1.0e-2, 'dm^2':1.0e-2, \
              'square inch':6.4516e-4}
    _unitsPreferred = ['m2', 'mm2', 'cm2']
    _uval_units = {'meter':2}


################################################################################
class BendingMoment(QuantityFloat):
    """Quantity bending moment

    >>> print(BendingMoment(1000.0*1.0, 'N.m', 'kN.m'))
       1.00  kN.m (BendingMoment)
    >>> print(BendingMoment(1000.0*0.200, 'N.m', 'kN.cm'))
      20.0   kN.cm (BendingMoment)
    """
    _isoUnit = 'N.m'
    _units = {'N.m':1.0, 'kN.m':1.0e3, 'kN.cm':10.0}
    _uval_units = {'meter':1+1, 'kilogram':1, 'second':-2}


################################################################################
class Boolean(QuantityBoolean):
    """Quantity  boolean

    >>> q = Boolean(True); print(q)
        True (Boolean)
    >>> q = Boolean(False); print(q)
       False (Boolean)
    >>> q = Boolean('T', 'T/F'); print(q)
        True (Boolean)
    >>> q = Boolean('F', 'T/F'); print(q)
       False (Boolean)

    >>> q = Boolean(True); print(q.__str__('T/F'))
           T (Boolean)
    >>> q = Boolean(False); print(q.__str__('T/F'))
           F (Boolean)

    """

TrueFalse = Boolean


################################################################################
class Density(QuantityFloat):
    """Quantity  density

    >>> d = Density(1.0, 'kg/m^3')
    >>> print(d)
       1.00  kg/m3 (Density)
    >>> print(d.get_str(unit='kg/m^3'))
       1.00  kg/m^3  (Density)
    >>> print(d.get_str(unit='to/m^3'))
       0.00100 to/m^3  (Density)
    >>> print(d.get_str(unit='kg/dm^3'))
       0.00100 kg/dm^3 (Density)
    """
    _isoUnit = 'kg/m3'
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'kg/m3',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}
    _units = {'kg/m3':1.0, 'kg/m^3':1.0, 'to/m3':1.0e+3, 'to/m^3':1.0e+3, 'kg/dm3':1.0e+3, 'kg/dm^3':1.0e+3}
    _uval_units = {'meter':-3, 'kilogram':1}


################################################################################
class Distance(QuantityDecimal):
    """quantity  distance

    >>> print(Distance(1.7, 'm'))
    1700.000 mm (Distance)
    >>> print(Distance('1.7', 'm', typecast=True))
    1700.000 mm (Distance)


    >>> L1 = Distance(1.7, 'm'); print(L1)
    1700.000 mm (Distance)
    >>> L2 = L1 + Distance(1.7, 'mm'); print(L2)
    1701.700 mm (Distance)

    >>> print(Distance('  1 ', 'm', typecast=True))
    1000.000 mm (Distance)
    >>> print(Distance('  d1 ', 'm', typecast=True))
    Traceback (most recent call last):
    ...
    ValueError: could not convert string to float: '  d1 '

    >>> print(Distance(1.0, 'm') - Distance(1.0, 'm'))
       0.000 mm (Distance)
    """
    _isoUnit = 'm'
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'mm',
                                                       'str_quantization':{'method':'1', 'precision':3}}}
    _unitsPreferred = ['mu', 'mm', 'm', 'km']
    _units = {'m':1.0, 'mu':1.0e-6, 'mm':1.0e-3, 'cm':1.0e-2, 'dm':1.0e-1, 'km':1.0e3, \
              'yard':0.9144, 'foot':0.3048, 'inch':25.4e-3, 'mile':1609.34, 'nautical mile':1853.18}
    _uval_units = {'meter':1}



################################################################################
class Energie(QuantityFloat):
    """Quantity  energie
    >>> W = Energie(Force(1.0, 'N').uval * Distance(1.0, 'm').uval); print(W)
       1.00  J (Energie)
    >>> W2 = Energie(1.0, 'eV'); print("%r" % W2)
    quantities.Energie(value=1.6021765314e-19, unit='J', displayUnit='J')
    """
    _isoUnit = 'J'
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'J',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}
    _units = {'J':1.0, 'mJ':1e-3, 'kJ':1e3, 'MJ':1e6, 'eV':1.6021765314e-19, 'kWh':1000.*60.*60.}
    _uval_units = {'meter':2, 'kilogram':1, 'second':-2}


################################################################################
class Flowrate(QuantityFloat):
    """Quantity  flowrate"""
    _isoUnit = 'm^3/sec'
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'Liter/min',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}
    _units = {'m^3/sec':1.0, 'Liter/min':1/(1000.0*60.0), 'm^3/h':1.0/(60.0*60.0)}
    _uval_units = {'meter':3, 'second':-1}

################################################################################
class FlowrateMass(QuantityFloat):
    """Quantity  flowrate mass"""
    _isoUnit = 'kg/sec'
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'kg/sec',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}
    _units = {'kg/sec':1.0, 'g/sec':1e-3}
    _uval_units = {'kilogram':1, 'second':-1}

################################################################################
class Force(QuantityFloat):
    """Quantity  force"""
    _isoUnit = 'N'
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'kN',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}
    _units = {'N':1.0, 'kN':1.0e3, 'MN':1.0e6, 'mN':1.0e-3, 'lbf':4.44822}
    _uval_units = {'meter':1, 'kilogram':1, 'second':-2}

################################################################################
class Frequency(QuantityFloat):
    """Quantity  frequency"""
    _isoUnit = '1/s'
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'Hz',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}
    _units = {'1/s':1.0, '1/sec':1.0, 'Hz':1.0}
    _uval_units = {'second':-1}


    def convert2VelocityAngular(self):
        return VelocityAngular(self.get_value('Hz') * 2 * scipy.constants.pi, 'rad/sec')


################################################################################
class Mass(QuantityFloat):
    """Quantity  mass"""
    _isoUnit = 'kg'
    _units = {'kg':1.0, 'g':1.0e-3, 'metr tonne':1.0e3, \
              'US ton':1016.05, 'pound':0.45359237, 'lb':0.45359237, 'ounce':28.3495e-3, 'oz':28.3495e-3}
    _uval_units = {'kilogram':1}
    _unitsPreferred = ['kg', 'g', 'metr tonne']
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'kg',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}

################################################################################
class MomentOfAreaFirst(QuantityFloat):
    """Quantity  first moment of area"""
    _isoUnit = 'm^3'
    _units = {'m^3':1.0, 'cm^3':10**(-3*2), 'mm^3':10**(-3*3)}
    _uval_units = {'meter':3}
    _displayUnitSystemList = {'mechanicalEngineering':'cm^3'}


################################################################################
class MomentOfInertiaOfMass(QuantityFloat):
    """Quantity  moment of inertia of mass

    >>> print((MomentOfInertiaOfMass(Mass(1.,'g')*Distance(1.,'cm')**2)))
       1.00  g.cm^2 (MomentOfInertiaOfMass)
    """
    _isoUnit = 'kg.m^2'
    _units = {'kg.m^2':1.0, 'kg.mm^2':1.0e-6, 'g.cm^2':1.0e-7}
    _uval_units = {'meter':2, 'kilogram':1}


################################################################################
class MomentOfAreaSecond(QuantityFloat):
    """MomentOfAreaSecond: bending, Ib

    dt: Widerstandsmoment

    see U{http://en.wikipedia.org/wiki/Second_moment_of_area}

    >>> I = MomentOfAreaSecond(1.0, 'mm^4', 'mm^4'); print(I)
       1.00  mm^4 (MomentOfAreaSecond)
    >>> I.set_displayUnit('m^4'); print(I)
       0.00000000000100 m^4 (MomentOfAreaSecond)
    """
    _isoUnit = 'm^4'
    _units = {'m^4':1.0, 'cm^4':10**(-4*2), 'mm^4':10**(-4*3)}
    _uval_units = {'meter':4}
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'cm^4',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}


MomentOfInertiaOfArea = MomentOfAreaSecond



################################################################################
class Number(QuantityInt):
    """Quantity  integer

    >>> print(Number(123))
     123     pcs (Number)

    """
    _isoUnit = 'pcs'
    _displayUnitSystemList = {None:{'displayUnit':'pcs',
                                    'str_quantization':{'method':'1', 'precision':0}},
                              'mechanicalEngineering':{'displayUnit':'pcs',
                                                       'str_quantization':{'method':'1', 'precision':0}}}
    _units = {'stk':1, 'pcs':1, '1':1}

    def __init__(self, value, unit=None, displayUnit=None, typecast=False):
        if unit is None and not isinstance(value, (Quantity, UVal)):
            unit = self._isoUnit
        QuantityInt.__init__(self, value, unit=unit, displayUnit=displayUnit, typecast=typecast)


################################################################################
class Pressure(QuantityFloat):
    """Quantity  pressure http://en.wikipedia.org/wiki/Pascal_%28unit%29"""
    _isoUnit = 'Pa'
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'bar',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}
    _unitsPreferred = ['Pa', 'MPa', 'bar']
    _units = {'Pa':1.0, 'kPa':1.0e3, 'bar':1.0e5, 'MPa':1.0e6,
              'psi':6894.757, 'lbf/in^2':6894.757, 'torr':133.322}
    _uval_units = {'meter':1-2, 'kilogram':1, 'second':-2}


################################################################################
class Power(QuantityFloat):
    """Quantity  Power"""
    _isoUnit = 'W'
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'kW',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}
    _units = {'W':1.0, 'kW':1.0e3, 'MW':1.0e6, 'GW':1.0e9, 'mW':1.0e-3, 'PS':735.49875}
    _uval_units = {'meter':2, 'kilogram':1, 'second':-3}


################################################################################
class Scalar(QuantityFloat):
    """Quantity  scalar

    http://de.wikipedia.org/wiki/Dezibel#Definition_von_Bel_und_Dezibel

    >>> print(Scalar(0.75,'1','%'))
      75.0   % (Scalar)
    >>> k =  Scalar(0.123456789,'1','%')
    >>> print(k.get_str())
      12.3   %       (Scalar)
    >>> s = k.get_str(**{'unit':'%', 'withQuantity':False, 'withUnit':False})
    >>> print(type(s))
    <class 'str'>
    >>> print(s)
      12.3  

    >>> k = Scalar(0.0, 'dB'); print(k)
       1.00   (Scalar)
    >>> k = Scalar(1.0, '1.0', displayUnit='dB'); print(k)
       0     dB (Scalar)
    >>> k = Scalar(10.0, '1.0', 'dB'); print(k)
      10.0   dB (Scalar)
    >>> k = Scalar(3.0, 'dB'); print(k)
       2.00   (Scalar)
    >>> k = Scalar(-40.0, 'dB'); print(k)
       0.000100  (Scalar)

    >>> k = Scalar(1.0, '1.0', 'Np'); print(k)
       0     Np (Scalar)
    >>> k = Scalar(1.0, 'Np'); print(k)
       2.72   (Scalar)

    """
    _isoUnit = '1.0'
    _unitsPreferred = ['1.0', '%']
    _units = {'1.0':1.0, '1':1.0, '':1.0, '%':0.01, 'dB':None, 'Np':None, 'Neper':None}
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}

    def __init__(self, value, unit=None, displayUnit=None, typecast=False):
        if unit is None and not isinstance(value, (Quantity, UVal)):
            unit = self._isoUnit
        QuantityFloat.__init__(self, value, unit=unit, displayUnit=displayUnit, typecast=typecast)


    def convert2iso(self, value, unit, typecast=False):
        """Quantity.convert2iso(value, unit) ... convert value from unit to iso-unit"""
        if  typecast:
            value = float(value)
        else:
            assert isinstance(value, float), 'value must be a float'
        if unit in ('dB',):
            return 10.0**(value/10.0)
        elif unit in ('Np', 'Neper'):
            return math.exp(value)
        else:
            return QuantityFloat.convert2iso(self, value=value, unit=unit, typecast=typecast)

    def convert2unit(self, value, unit):
        """Quantity.convert2unit(value, unit) ... convert value from iso-unit to unit"""
        assert isinstance(value, float), 'value must be a float: %s' % value
        if unit in ('dB',):
            return 10.0 * math.log10(value)
        elif unit in ('Np', 'Neper'):
            return math.log(value)
        else:
            return QuantityFloat.convert2unit(self, value=value, unit=unit)


################################################################################
class SectionModulus(QuantityFloat):
    """Section Modulus"""
    _isoUnit = 'm^3'
    _units = {'m^3':1.0, 'cm^3':10**(-3*2), 'mm^3':10**(-3*3)}
    _uval_units = {'meter':3}
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'cm^3',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}


################################################################################
class Speed(QuantityFloat):
    """Quantity  speed"""
    _isoUnit = '1/s'
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'rpm',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}
    _units = {'1/s':1.0, '1/sec':1.0, 'Hz':1.0, 'rpm':1.0/60.0}
    _uval_units = {'second':-1}

################################################################################
class Stress(QuantityFloat):
    """Quantity  stress"""
    _isoUnit = 'Pa'
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'N/mm^2',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}
    _units = {'Pa':1.0, 'N/m^2':1.0, 'N/mm^2':1.0e6, 'N/mm2':1.0e6, 'MPa':1.0e6, }
    _uval_units = {'meter':1-2, 'kilogram':1, 'second':-2}
    _unitsPreferred = ['Pa', 'N/mm^2', 'MPa']


################################################################################
class SpringConstant(QuantityFloat):
    """Quantity  Spring Stiffness

    F = -k*x

    >>> k = SpringConstant(1.0, 'N/m', displayUnit='N/mm')
    >>> print(k)
       0.00100 N/mm (SpringConstant)
    """
    _isoUnit = 'N/m'
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'N/mm',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}
    _units = { 'N/m':1.0, 'N/mm':1.0e3}
    _uval_units = {'meter':1-1, 'kilogram':1, 'second':-2}


################################################################################
class SpringConstantTorsion(QuantityFloat):
    """Quantity  Spring Stiffness

    M = -k*phi

    >>> SpringConstantTorsion(1.0, 'N*m/rad', displayUnit='N*m/rad')
    quantities.SpringConstantTorsion(value=1.0, unit='N*m/rad', displayUnit='N*m/rad')

    """
    _isoUnit = 'N*m/rad'
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'N/mm',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}
    _units = { 'N*m/rad':1.0}
    _uval_units = {'meter':1+1, 'kilogram':1, 'second':-2}


################################################################################
class Text(QuantityString):
    """Quantity Text

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
    >>> cmp = lambda x, y: (x > y) - (x < y) 
    >>> print(cmp(s1, s3))
    -1

    """

String = Text

################################################################################
class TemperatureAbsolute(QuantityFloatOffset):
    """Quantity  temperatureAbsolute

        >>> Quantity.set_str_quantization(None)
        >>> print(TemperatureAbsolute(20.0, 'K', 'K'))
          20.0   K (TemperatureAbsolute)
        >>> print(TemperatureAbsolute(20.0, 'degC', 'K'))
         293     K (TemperatureAbsolute)
        >>> print(TemperatureAbsolute(20.0, 'degF', 'K'))
         471     K (TemperatureAbsolute)

        >>> print(TemperatureAbsolute(0.0, 'degF', 'K'))
         460     K (TemperatureAbsolute)
        >>> Ta1 = TemperatureAbsolute(0.0, 'degC', 'K'); print(Ta1)
         273     K (TemperatureAbsolute)
        >>> Ta2 = TemperatureAbsolute(0.0, 'K', 'K'); print(Ta2)
           0     K (TemperatureAbsolute)
        >>> Td = Ta1 + Ta2
        Traceback (most recent call last):
        ...
        EngineeringTools.quantities.quantitiesbase.ParaDInF_quantity_Error: add of absolute temperature is not possible
        >>> Td = Ta1 - Ta2; print(Td)
         273     K (TemperatureDifferential)
        >>> print(Ta2 + Td)
         273     K (TemperatureAbsolute)

    """

    _isoUnit = 'K'
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'degC',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}
    _units = {'K':(1.0, 0.0), 'degC':(1.0, 273.15), 'degF':(5.0/9.0, 459.67)}
    _uval_units = {'kelvin':1}
    _unitsPreferred = ['K', 'degC']

    def __add__(self, obj):
        """add

        add
            - add of differential temperature and absolute temperature
            - add of absolute temperature is not possible

        """
        if isinstance(obj, TemperatureAbsolute):
            raise ParaDInF_quantity_Error('add of absolute temperature is not possible')
        elif isinstance(obj, TemperatureDifferential):
            return TemperatureAbsolute(self.get_value() + obj.get_value(), self.get_isoUnit(), self.get_displayUnit())
        else:
            raise ParaDInF_quantity_ErrorQuantitiesDoNotMatch()

    def __sub__(self, obj):
        """sub two TemperatureAbsolute"""
        if isinstance(obj, self.__class__):
            return TemperatureDifferential(self.get_value() - obj.get_value(), self.get_isoUnit(), self.get_displayUnit())
        else:
            raise ParaDInF_quantity_ErrorQuantitiesDoNotMatch()



################################################################################
class TemperatureDifferential(QuantityFloat):
    """Quantity  temperatureDifferential"""
    _isoUnit = 'K'
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'C',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}
    _units = {'K':1.0, 'degC':1.0, 'degF':5.0/9.0}
    _uval_units = {'kelvin':1}
    _unitsPreferred = ['K', 'degC']

################################################################################
class Time(QuantityFloat):
    """Quantity  time"""
    _isoUnit = 's'
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'sec',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}
    _units = {'us':1e-6, 'ms':0.001, 'sec':1.0, 's':1.0, 'min':60.0, 'h':60.0*60.0,
              'd':24.0*60.0*60.0, 'a':365.25*24.0*60.0*60.0}
    _uval_units = {'second':1}


Duration = Time


################################################################################
class Torque(QuantityFloat):
    """Quantity  torque"""
    _isoUnit = 'N*m'
    _units = {'N.m':1.0, 'kN.m':1.0e3, 'mN.m':1.0e-3, 'N.mm':1.0e-3, 'lbf.in':0.1129848, 'N*m':1.0}
    _uval_units = {'meter':1+1, 'kilogram':1, 'second':-2}
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'N.m',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}


################################################################################
class ViscosityDynamic(QuantityFloat):
    """Quantity  ViscosityDynamic

    >>> print(ViscosityDynamic(1.0, 'Pa*sec', displayUnit='mPa*sec'))
    1000     mPa*sec (ViscosityDynamic)
    """
    _isoUnit = 'Pa*sec'
    _units = {'Pa*sec':1.0, 'mPa*sec':1.0e-3}
    _uval_units = {'meter':1-2, 'kilogram':1, 'second':-1}
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'mPa*sec',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}


################################################################################
class ViscosityKinematic(QuantityFloat):
    """Quantity  ViscosityKinematic

    >>> print(ViscosityKinematic(1.0, 'mm^2/sec', displayUnit='m^2/sec'))
       0.00000100 m^2/sec (ViscosityKinematic)
    >>> print(ViscosityKinematic(1.0, 'St', displayUnit='m^2/sec'))
       0.000100 m^2/sec (ViscosityKinematic)
    >>> print(ViscosityKinematic(1.0, 'cm^2/sec', displayUnit='m^2/sec'))
       0.000100 m^2/sec (ViscosityKinematic)
    >>> print(ViscosityKinematic(1.0, 'cSt', displayUnit='m^2/sec'))
       0.00000100 m^2/sec (ViscosityKinematic)
    """
    _isoUnit = 'm^2/sec'
    _units = {'m^2/sec':1.0, 'mm^2/sec':1.0e-6, 'cm^2/sec':1.0e-4, 'St':1.0e-4, 'cSt':1.0e-6}
    _uval_units = {'meter':2, 'second':-1}
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'mm^2/sec',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}

################################################################################
class Velocity(QuantityFloat):
    """Quantity  Velocity

    >>> v=Velocity(1.0, 'c0'); print('%r' % v)
    quantities.Velocity(value=299792458.0, unit='m/sec', displayUnit='m/sec')
    """
    _isoUnit = 'm/sec'
    _units = {'m/sec':1.0, 'm/s':1.0, 'km/h':1000.0/(60*60), 'c0':299792458.0}
    _uval_units = {'meter':1, 'second':-1}
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'m/sec',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}
    _unitsPreferred = ['m/sec', 'km/h']



################################################################################
class VelocityAngular(QuantityFloat):
    """Quantity Angular Velocity"""
    _isoUnit = 'rad/sec'
    _units = {'rad/sec':1.0}  #  dangerous, '1/sec':1.0}
    _uval_units = {'second':-1}
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'rad/sec',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}
    _unitsPreferred = ['rad/sec']

    def convert2Frequency(self):
        return Frequency(self.get_value('rad/sec') / (2* scipy.constants.pi), 'Hz')



################################################################################
class Volume(QuantityFloat):
    """Quantity  volume"""
    _isoUnit = 'm3'
    _units = {'m3':1.0, 'm^3':1.0, 'mm3':1.0e-9, 'mm^3':1.0e-9, 'cm^3':1.0e-6, 'cm3':1.0e-6, 'dm^3':1.0e-3, \
              'Liter':1.0e-3, 'mL':1e-6, 'gallon':4.54609e-3, 'USgal':3.78541e-3}
    _uval_units = {'meter':3}


################################################################################
# test
################################################################################
def _setup_doctest():
    from EngineeringTools import quantities as ETQ # pylint: disable=reimported,import-outside-toplevel
    ETQ.Quantity.set_displayUnitSystem('mechanicalEngineering')

#eof

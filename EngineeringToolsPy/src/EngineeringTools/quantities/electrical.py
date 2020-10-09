#!/usr/bin/env python3
# pylint: disable=line-too-long
'''

'''

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"


__all__ = ["Voltage", "Current", "Resistance"]


from . import quantitiesbase as base


################################################################################
class Voltage(base.QuantityFloat):
    """Quantity  Voltage
https://en.wikipedia.org/wiki/Volt
    """
    _isoUnit = 'V'
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'V',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}
    _units = {'V':1.0, 'kV':1000.0, 'mV':1.0e-3}
    _uval_units = {'meter':2, 'kilogram':1, 'second':-3, 'ampere':-1}
    _unitsPreferred = ['V', 'kV', 'mV']


################################################################################
class Current(base.QuantityFloat):
    """Quantity  Current
https://en.wikipedia.org/wiki/Electric_current
https://en.wikipedia.org/wiki/Ampere
"""
    _isoUnit = 'A'
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'A',
                                                       'str_quantization':{'method':'1r', 'precision':3}}}
    _units = {'A':1.0, 'kA':1000.0, 'mA':1.0e-3}
    _uval_units = {'ampere':1}
    _unitsPreferred = ['A', 'kA', 'mA']



################################################################################
class Resistance(base.QuantityFloat):
    """Quantity  Resistance
https://en.wikipedia.org/wiki/Ohm
    """
    _isoUnit = 'Ohm'
    _displayUnitSystemList = {'mechanicalEngineering':{'str_quantization':{'method':'1r', 'precision':3}}}
    _units = {'Ohm':1.0, 'kOhm':1000.0, 'MOhm':1.0e6, 'mOhm':1.0e-3}
    _uval_units = {'meter':2, 'kilogram':1, 'second':-3, 'ampere':-2}
    _unitsPreferred = ['Ohm', 'kOhm', 'MOhm', 'mOhm']



################################################################################
class Inductance(base.QuantityFloat):
    """Quantity Inductance
https://en.wikipedia.org/wiki/Inductance
https://en.wikipedia.org/wiki/Henry_(unit)
    """
    _isoUnit = 'H'
    _displayUnitSystemList = {'mechanicalEngineering':{'str_quantization':{'method':'1r', 'precision':3}}}
    _units = {'H':1.0, 'mH':1.0e-3}
    _uval_units = {'meter':2, 'kilogram':1, 'second':-2, 'ampere':-2}
    _unitsPreferred = ['H', 'mH']

# eof

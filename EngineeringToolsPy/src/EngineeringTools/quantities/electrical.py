#!/usr/bin/env python3
# pylint: disable=line-too-long
'''

'''

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"


__all__ = ["Voltage", "Current", "Resistance", "Inductance", "MemorySize"]



# run doctest, workaround relative import
if __name__ == '__main__':
    import sys
    import doctest # pylint: disable=import-outside-toplevel
    from EngineeringTools import quantities as ETQ             # pylint: disable=reimported,import-outside-toplevel
    ETQ.Quantity.set_displayUnitSystem('mechanicalEngineering')
    module_name = 'EngineeringTools.quantities.electrical'      # pylint: disable=invalid-name
    module = __import__(module_name, fromlist=['*'], level=0)  # pylint: disable=invalid-name
    module._setup_doctest()                                    # pylint: disable=protected-access
    print(doctest.testmod(module, optionflags=doctest.ELLIPSIS))
    sys.exit()



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




################################################################################
class MemorySize(base.QuantityFloat):  # FIXME: How to round, represent
    """Quantity MemorySize

    https://en.wikipedia.org/wiki/Megabyte

    >>> print(MemorySize(1, 'Byte', displayUnit='Byte'))
       1.000 Byte (MemorySize)
    >>> print(MemorySize(1, 'KB', displayUnit='Byte'))
    1000     Byte (MemorySize)
    >>> print(MemorySize(1, 'KiB', displayUnit='Byte'))
    1024     Byte (MemorySize)

    >>> print(MemorySize(1.23456789, 'Byte'))
       1.235 Byte (MemorySize)

    >>> print(MemorySize(1.23456789, 'KiB'))
       1.235 KiB (MemorySize)

    """
    _isoUnit = 'Byte'
    _units = {'Byte':1, 'Bit8':1./8,
              'KB':1000,    'KiB':2**10, 
              'MB':1000**2, 'MiB':(2**10)**2,
              'GB':1000**3, 'GiB':(2**10)**3,
              'TB':1000**4, 'TiB':(2**10)**4,
              'PB':1000**5, 'PiB':(2**10)**5}
    _displayUnitSystemList = {'mechanicalEngineering':{'str_quantization':{'method':'1r', 'precision':4}}}
    _uval_units = {}
    _unitsPreferred = ['KiB', 'MiB', 'GiB', 'TiB']



################################################################################
# test
################################################################################
def _setup_doctest():
    from EngineeringTools import quantities as ETQ # pylint: disable=reimported,import-outside-toplevel
    ETQ.Quantity.set_displayUnitSystem('mechanicalEngineering')



# eof

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
'''

'''

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"


__all__ = ["Money", "MoneyPerTime"]


# run doctest, workaround relative import
if __name__ == '__main__':
    import sys
    import doctest # pylint: disable=import-outside-toplevel
    from EngineeringTools import quantities as ETQ             # pylint: disable=reimported,import-outside-toplevel
    ETQ.Quantity.set_displayUnitSystem('mechanicalEngineering')
    module_name = 'EngineeringTools.quantities.money'      # pylint: disable=invalid-name
    module = __import__(module_name, fromlist=['*'], level=0)  # pylint: disable=invalid-name
    module._setup_doctest()                                    # pylint: disable=protected-access
    print(doctest.testmod(module, optionflags=doctest.ELLIPSIS))
    sys.exit()


import logging
from . import quantitiesbase as base
from ..uval import UVal

log = logging.getLogger('ParaDIn.quantity.money')
log.critical('Attention: update currency rats!  >>> Moneyupdate_currency_rate(currency, rate_EURO)')

UVal.add_base_unit('EURO', 'EURO')



################################################################################
class Money(base.QuantityFloat):
    """
    """
    _isoUnit = 'EURO'
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'SEK',
                                                       'str_quantization':{'method':'1', 'precision':0}}}
    _units = {'EURO':1, 'SEK':0.1 }
    _uval_units = {'EURO':1, }
    _unitsPreferred = ['SEK', ]


    @classmethod
    def update_currency_rate(cls, currency, rate_EURO):
        cls._units[currency] = rate_EURO



################################################################################
class MoneyPerTime(base.QuantityFloat):
    """
    """
    _isoUnit = 'EURO/sec'
    _displayUnitSystemList = {'mechanicalEngineering':{'displayUnit':'SEK/h',
                                                       'str_quantization':{'method':'1', 'precision':0}}}
    _units = {'EURO/sec':1, 'EURO/h':1/(60*60), 'SEK/h':Money._units['SEK']/(60*60) }
    _uval_units = {'EURO':1, 'second':-1}
    _unitsPreferred = ['SEK/h', ]


################################################################################
# test
################################################################################
def _setup_doctest():
    from EngineeringTools import quantities as ETQ # pylint: disable=reimported,import-outside-toplevel
    ETQ.Quantity.set_displayUnitSystem('mechanicalEngineering')

# eof

#!/usr/bin/env python3
# pylint: disable-msg=line-too-long,wrong-import-position,bad-whitespace
"""run all doctests
"""

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"

import os
import sys
import doctest

ppath = os.path.join(os.path.dirname(os.getcwd()), 'src')  # pylint: disable=invalid-name
sys.path.insert(0, ppath)
import EngineeringTools.quantities as Q

# ------------------------------------------------------------------------
MODULE_LIST = ['EngineeringTools.qnt', 'EngineeringTools.uval', 'EngineeringTools.quantities.quantitiesbase', 'EngineeringTools.quantities',
               'EngineeringTools.quantities.electrical', 'EngineeringTools.quantities.mechanics', 'EngineeringTools.quantities.money',
               'EngineeringTools.tools.functions', 'EngineeringTools.tools.calc', 'EngineeringTools.tools.interpolate', 'EngineeringTools.tools.geo_circle', 'EngineeringTools.tools.volume',
               'EngineeringTools.mechanical_eng.material', 'EngineeringTools.mechanical_eng.buckling', 'EngineeringTools.mechanical_eng.beamsection',
               'EngineeringTools.fluidpower_eng.cylinder', 'EngineeringTools.fluidpower_eng.hydraulicServoSystem', 'EngineeringTools.fluidpower_eng.oil', 'EngineeringTools.fluidpower_eng.orifice', 'EngineeringTools.fluidpower_eng.proportionalValve'
                ]


def do_doctest(module_list):
    """run doctest on modules in MODULE_LIST"""

    Q.Quantity.set_displayUnitSystem('mechanicalEngineering')

    result = []
    for module_name in module_list:
        print('\n\n')
        print('-'*80)
        print(module_name)
        print('-'*80)
        res = {}
        res['name'] = module_name
        module = __import__(module_name, fromlist=['*'], level=0)
        res['file'] = module.__file__

        if hasattr(module, '_setup_doctest'):
            module._setup_doctest()  # pylint: disable=protected-access
        res['doctest'] = doctest.testmod(module, optionflags=doctest.ELLIPSIS)

        result.append(res)
    return result


def run_doctests(module_list):
    """Run DocTest for modules in list
    """
    result = do_doctest(module_list)
    for res in  result:
        print(res)

    print('-' * 80)

    fails = 0
    for res in  result:
        if res['doctest'][0] != 0:
            print(res)
            fails += res['doctest'][0]
    print('%s doctests Faild' % fails)
    if fails > 0:
        sys.exit(1)



if __name__ == '__main__':
    run_doctests(MODULE_LIST)
    #run_doctests(['EngineeringTools.tools.calc',])

# eof

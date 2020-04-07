#!/usr/bin/env python3
# pylint: disable-msg=line-too-long,missing-function-docstring,missing-class-docstring,empty-docstring,bad-whitespace

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"

import unittest

import os
import sys
ppath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'src') # pylint: disable=invalid-name
sys.path.insert(0, ppath)

import EngineeringTools.quantities as ETQ
import EngineeringTools.mechanical_eng.material as ETMmat
ETQ.Quantity.set_displayUnitSystem('mechanicalEngineering')


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_steel_init(self):
        ms = ETMmat.Steel()

    def test_Steel_S355JR_init(self):
        ms = ETMmat.Steel_S355JR()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

# eof

#!/usr/bin/env python3
# pylint: disable-msg=line-too-long,missing-function-docstring,missing-class-docstring,empty-docstring,bad-whitespace

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"

import os
import sys
ppath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'src') # pylint: disable=invalid-name
sys.path.insert(0, ppath)

import unittest

import EngineeringTools.quantities as ETQ
import EngineeringTools.mechanical_eng.buckling as ETMB

class Test(unittest.TestCase):


    def setUp(self):
        ETQ.Quantity.set_displayUnitSystem('mechanicalEngineering')

    def tearDown(self):
        pass


#     def test_momentOfArea2nd(self):
#         buckling = ETMB.Buckling()
#         self.assertIsInstance(buckling, ETMB.Buckling)
#         with self.assertRaises(ETQ.ParaDInF_quantity_ErrorUnitNotFound):
#             buckling.momentOfArea2nd = 1
#         I = ETQ.MomentOfAreaSecond(1., 'mm^4')
#         buckling.momentOfArea2nd = I 
#         self.assertEqual(buckling.momentOfArea2nd, I)
#         self.assertIsNot(buckling.momentOfArea2nd, I)
        



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

# eof

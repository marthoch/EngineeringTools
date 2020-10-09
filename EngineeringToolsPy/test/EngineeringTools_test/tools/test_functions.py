#!/usr/bin/env python3
# pylint: disable-msg=line-too-long,missing-function-docstring,missing-class-docstring,empty-docstring

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"

import unittest
import os
import sys
ppath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'src') # pylint: disable=invalid-name
sys.path.insert(0, ppath)

import EngineeringTools.quantities as ETQ
import EngineeringTools.tools.functions as ETF


class Test(unittest.TestCase):

    def setUp(self):
        ETQ.Quantity.set_displayUnitSystem('mechanicalEngineering')

    def tearDown(self):
        pass

    def test_power(self):
        with self.assertRaises(ETF.EngineeringTools_tools_Error_units):
            ETF.power("a", 2.)
        with self.assertRaises(ETF.EngineeringTools_tools_Error_units):
            ETF.power(2., "a")
        self.assertEqual(ETF.power(3., 2.), 9.)
        self.assertEqual(ETF.power(3, 2), 9.)
        self.assertEqual(ETF.power(3, -2.), 1/9.)

        self.assertEqual(ETF.power(ETQ.Distance(2., 'm').uval, 2), ETQ.Distance(2., 'm').uval*ETQ.Distance(2., 'm').uval)
        self.assertEqual(ETF.power(ETQ.Distance(2., 'm'), 2),      ETQ.Distance(2., 'm').uval*ETQ.Distance(2., 'm').uval)
        self.assertEqual(ETF.power(ETQ.Distance(2., 'm'), ETQ.Number(2)),      ETQ.Distance(2., 'm').uval*ETQ.Distance(2., 'm').uval)
        self.assertEqual(ETF.power(ETQ.Distance(2., 'm'), ETQ.Scalar(2.)),     ETQ.Distance(2., 'm').uval*ETQ.Distance(2., 'm').uval)


    def test_physical_constants(self):
        with self.assertRaises(KeyError):
            ETF.physical_constants('test')
        self.assertEqual(ETF.physical_constants('Stefan-Boltzmann constant'), 5.670374419e-08*ETQ.Power(1,'W')/ETQ.Area(1,'m2')/ETQ.TemperatureAbsolute(1,'K')/ETQ.TemperatureAbsolute(1,'K')/ETQ.TemperatureAbsolute(1,'K')/ETQ.TemperatureAbsolute(1,'K'))  # (5.670374419e-08, 'W m^-2 K^-4', 0.0)
        ETF.physical_constants('hyperfine transition frequency of Cs-133')
        ETF.physical_constants('conventional value of von Klitzing constant')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
# eof

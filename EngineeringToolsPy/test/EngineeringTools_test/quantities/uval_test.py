#!/usr/bin/env python3
# pylint: disable-msg=line-too-long,missing-function-docstring,missing-class-docstring,empty-docstring,bad-whitespace
"""
"""

import os
import sys
import unittest

ppath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'src') # pylint: disable=invalid-name
sys.path.insert(0, ppath)
import EngineeringTools.uval as QUVal # pylint: disable=wrong-import-position



class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass



    def test__sub(self):
        L1 = QUVal.UVal(1., {'meter':1})
        L2 = QUVal.UVal(2., {'meter':1})
        self.assertEqual(1., (L2-L1).get_value())


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

# eof

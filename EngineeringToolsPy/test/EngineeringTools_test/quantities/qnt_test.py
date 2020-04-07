#!/usr/bin/env python3
# pylint: disable-msg=line-too-long,missing-function-docstring,missing-class-docstring,empty-docstring,bad-whitespace
"""
"""

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"

import os
import sys
import unittest

ppath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'src') # pylint: disable=invalid-name
sys.path.insert(0, ppath)
import EngineeringTools.qnt as qnt # pylint: disable=wrong-import-position

class Test(unittest.TestCase):


    def test__quant(self):
        self.assertEqual(1235.0, qnt.quant(1234.56789, '1'))

    def test__format(self):
        self.assertEqual('     1 234.568', qnt.quant(1234.56789, '1', 3, rettype='string'))



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

# eof

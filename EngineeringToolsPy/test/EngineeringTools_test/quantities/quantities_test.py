#!/usr/bin/env python3
# pylint: disable-msg=

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"

# $Source$

import math
import os
import sys
from fractions import Fraction
import unittest

ppath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'src') 
sys.path.insert(0, ppath)
import EngineeringTools.quantities as Q
import EngineeringTools.quantities as ETQ

################################################################################
#  unit test
################################################################################

class TestSequenceFunctions(unittest.TestCase):


    def test__format(self):
        self.assertEqual(str(ETQ.Scalar(12.3456789)),   '        12.3    (Scalar)')
        self.assertEqual(str(ETQ.Scalar(0.0123456789)), '         0.0123  (Scalar)')



    def test__selftest_lists(self):
        import inspect

        def do_test(cls):
            self.assertTrue(cls._isoUnit in cls._units)
            for u in cls._units:
                self.assertTrue(isinstance(u, str))
            if hasattr(cls, '_unitsPreferred'):
                for u in cls._unitsPreferred:
                    self.assertTrue(isinstance(u, str))
                    self.assertTrue(u in cls._units)


        for member in inspect.getmembers(Q):
            if inspect.isclass(member[1]) and  issubclass(member[1], Q.Quantity):
                #print(member[0])
                do_test(member[1])


    def Xtest__Quantity(self):
        L1 = 1
        q = Q.Quantity(L1)
        self.assertRaises(Q.ParaDInF_quantity_ErrorUnitNotFound, q.set_value, L1, 'xyz')
        self.assertRaises(Q.ParaDInF_quantity_ErrorUnitNotFound, q.set_displayUnit, 'xyz')
        d1 = Q.Distance(1.23, 'm', 'mm')
        d2 = Q.Distance(2.34, 'km', 'cm')
        m = Q.Mass(1.23, 'kg', 'kg')
        d1.check_match_quantities(d2)
        self.assertRaises(Q.ParaDInF_quantity_ErrorQuantitiesDoNotMatch, d1.check_match_quantities, m)

    def Xtest__QuantityDecimal(self):
        L1 = 1.23456789
        q = Q.QuantityDecimal(L1)
        self.assertRaises(AssertionError, Q.QuantityDecimal, 123)

    def Xtest__QuantityFloat(self):
        L1 = 1.23456789
        q = Q.QuantityFloat(L1)
        self.assertRaises(AssertionError, Q.QuantityFloat, 123)

    def Xtest__QuantityInt(self):
        q = Q.QuantityInt(123)
        self.assertRaises(AssertionError, Q.QuantityInt, 123.0)

    def test__Angle(self):
        A1 = 0.5
        qa = Q.Angle(A1, 'rad', 'deg')
        self.assertEqual(A1, qa.get_value())
        self.assertEqual(A1, qa.get_value(unit='rad'))
        self.assertEqual(qa.get_value(), qa.get_value(unit=qa.get_isoUnit()))
        self.assertAlmostEqual(A1/math.pi*180, qa.get_value(unit='deg'), 9)


    def test__Area(self):
        L1 = 1.23456789
        A1 = L1**2
        qd = Q.Distance(L1, 'm', 'mm')
        qa = Q.Area(A1, 'm^2', 'mm^2')             
        self.assertAlmostEqual(A1, qa.get_value(), 9)
        self.assertAlmostEqual(A1, qa.get_value(unit='m^2'), 9)       
        self.assertEqual(qa.get_value(unit=qa.get_isoUnit()), qa.get_value()) 
        for (ud, ua) in [('m', 'm^2'), ('mm', 'mm^2'), ('cm', 'cm^2'), ('dm', 'dm^2'), ('inch', 'square inch')]:
            self.assertAlmostEqual(qd.get_value(unit=ud)**2, qa.get_value(unit=ua), 9, ('%f %s **2 != %f %s' % (qd.get_value(unit=ud)**2, ud, qa.get_value(unit=ua), ua)))    

    def test__Distance(self):        
        L1 = 1.23456789
        qd = Q.Distance(L1, 'm', 'mm')             
        self.assertEqual(L1, qd.get_value())
        self.assertEqual(L1, qd.get_value(unit='m'))        
        self.assertEqual(qd.get_value(unit=qd.get_isoUnit()), qd.get_value())
        self.assertAlmostEqual(L1*1.0e3, qd.get_value(unit='mm'), 9)
        self.assertAlmostEqual(L1*1.0e2, qd.get_value(unit='cm'), 9)
        self.assertAlmostEqual(L1/1.0e3, qd.get_value(unit='km'), 9)

    def test__Number(self):
        qn = Q.Number(123)        

    def test__Speed(self):
        f = 50.0
        qs = Q.Speed(f, 'Hz')
        self.assertAlmostEqual(qs.get_value(unit='rpm')/60.0, qs.get_value(unit='1/sec'), 9)

    def test__Temperature(self):
        Td = 23.4
        Ta = Td
        qTd = Q.TemperatureDifferential(Td, 'K', 'K')
        qTa = Q.TemperatureAbsolute(Ta, 'K', 'degC')
        self.assertAlmostEqual(Td, qTd.get_value(), 9) 
        self.assertAlmostEqual(Ta, qTa.get_value(), 9)
        self.assertAlmostEqual(qTd.get_value(unit='K'), qTd.get_value(unit='degC'), 9)
        self.assertAlmostEqual(qTa.get_value(unit='K'), qTa.get_value(unit='degC')+273.15, 9)
        self.assertAlmostEqual(qTd.get_value(unit='K'), qTa.get_value(unit='K'), 9)
        self.assertAlmostEqual(qTd.get_value(unit='degC'), qTa.get_value(unit='K'), 9)
        self.assertAlmostEqual(qTd.get_value(unit='degF'), qTd.get_value(unit='K')*9.0/5.0, 9)
        self.assertAlmostEqual(qTd.get_value(unit='degF'), qTd.get_value(unit='degC')*9.0/5.0, 9)
        self.assertAlmostEqual(qTa.get_value(unit='degF'), 9.0/5.0*qTa.get_value(unit='K')-459.67, 9)
        self.assertAlmostEqual(qTa.get_value(unit='degF'), 9.0/5.0*qTa.get_value(unit='degC')+32.0, 9)

    def test__Velocity(self):
        s = 123.0
        t = 1.1
        v = s/t
        qs = Q.Distance(s, 'm')
        qt = Q.Time(t, 'sec')
        qv = Q.Velocity(v, 'm/sec')
        self.assertAlmostEqual(qv.get_value(unit='m/sec'), qs.get_value(unit='m')/qt.get_value(unit='sec'), 9)
        self.assertAlmostEqual(qv.get_value(unit='km/h'), qs.get_value(unit='km')/qt.get_value(unit='h'), 9)
        
    def test__Volume(self):
        L1 = 1.23456789 
        V1 = L1**3
        qd = Q.Distance(L1, 'm', 'mm')
        qv = Q.Volume(V1, 'm^3', 'mm^3')
        self.assertTrue(len(qv.__doc__) > 10, 'no or short doc-string')
        self.assertAlmostEqual(V1, qv.get_value(), 9)
        self.assertAlmostEqual(V1, qv.get_value(unit='m^3'), 9)
        self.assertEqual(qv.get_value(unit=qv.get_isoUnit()), qv.get_value())
        self.assertAlmostEqual(qd.get_value(unit='mm')**3, qv.get_value(unit='mm^3'), 9)
        for (ud, uv) in [('m', 'm^3'), ('mm', 'mm^3'), ('cm', 'cm^3'), ('dm', 'dm^3')]:
            self.assertAlmostEqual(qd.get_value(unit=ud)**3, qv.get_value(unit=uv), 9, ('%f %s **3 != %f %s' % (qd.get_value(unit=ud)**3, ud, qv.get_value(unit=uv), uv)))


    @unittest.skip("does not work after separating qunatities in various packages")
    def test__generateQuantity(self): 
        a = Q.generateQuantity('Distance', 1.22, 'm')
        a = Q.generateQuantity(**{'quantity':'Distance', 'value':1.22, 'unit':'m'})
        x = a.get_as_dict()

    def test__copy(self): 
        a = Q.Distance( 1.22, 'm')
        b = a.copy()


    def test__get_value(self):        
        L1 = 1.23456789
        qd = Q.Distance(L1, 'm', 'mm')
        # unit default                     
        self.assertEqual(L1, qd.get_value())        
        # unit None                     
        self.assertEqual(L1, qd.get_value(unit=None))
        # unit m                     
        self.assertEqual(L1, qd.get_value(unit='m'))
        # unit not existing
        self.assertRaises(AssertionError, qd.get_value, unit='xyzabc')


    def test__QuantityBoolean__convert2iso(self):
        qtest = Q.QuantityBoolean(True)
        # standard
        self.assertEqual(qtest.convert2iso(True, 'boolean'), True)
        self.assertEqual(qtest.convert2iso('T', 'T/F'), True)
        # typecast=True
        self.assertRaises(NotImplementedError, qtest.convert2iso, True, 'boolean', typecast=True)
        # wrong type of value
        self.assertRaises(AssertionError, qtest.convert2iso, 111, 'boolean')

        # wrong unit
        #self.assertEqual(qtest.convert2iso(True, 'XXX'), True)

    def test__pow(self):
        d = ETQ.Distance(2, 'm')
        self.assertEqual(d**2, ETQ.UVal(4,{'meter': Fraction(2, 1)}))
        self.assertEqual(ETQ.Area(4, 'm2')**(1/2), ETQ.UVal(2,{'meter': Fraction(1, 1)}))

    def test__1(self): 
        Q.Quantity.set_displayUnitSystem('mechanicalEngineering')
        d = Q.Distance(1.1, 'm')


def my_test():
    Q.Quantity.set_displayUnitSystem('mechanicalEngineering')
    d = Q.Distance(1.1, 'm')
    print(repr(d))
    print(d.get_unitsPreferred())

    print('-'*10)
    d2 = Q.Distance(2.1, 'm', 'km')
    print(repr(d2))
    print(d2)
    x = d2.get_value('m')
    print(x)

    d = Q.Distance(1.1, 'm')
    print(repr(d))

    s1 = d.get_uval() / (3*d.get_uval())
    s1 = Q.Scalar(s1)
    print(s1)

    s2 = d.get_uval() / 3

    print(s2)


def speedtest():

    import timeit

    stmt = """
    q_FlowRate = quantities.Flowrate(100.0, 'm^3/h')
    q_FlowVelocity = quantities.Velocity(1.5, 'm/sec')
    uval_V_dt = q_FlowRate.get_uval()
    uval_v = q_FlowVelocity.get_uval()
    uval_d = sqrt((4.0 / PI.uval * uval_V_dt / uval_v))
    q_Diameter = quantities.Distance(uval_d)
    """
    N = 1000
    t = timeit.Timer(stmt=stmt, setup='from EngineeringTools import quantities; from EngineeringTools.tools.functions import PI, sqrt')
    time = t.timeit(number=N)/float(N)
    print("%20s %.2f mu sec/pass" % (stmt, 1e6*time))
    print("%20s %.2f pass/sec" % (stmt, 1/time))


# ------------------------------------------------------------------------
if __name__ == '__main__':
#     from paradinf import loggingconf   
#     loggingconf.loggingconf()

    print('\n%s\n##my_test\n' % ('-'*75))
    my_test()
    print('\n%s\n##speedtest\n' % ('-'*75))
    speedtest()
    print('\n%s\n##unittest\n' % ('-'*75))
    unittest.main()
    
# eof --------------------------------------------------------------------


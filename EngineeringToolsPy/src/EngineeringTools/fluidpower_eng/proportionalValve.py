#!/usr/bin/env python3
# pylint: disable-msg=line-too-long,missing-module-docstring,missing-function-docstring,missing-class-docstring,no-else-return,invalid-name,multiple-statements

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"


import numpy as np
from .. import quantities as Q
from .. import quantities as ETQ
from EngineeringTools.tools import functions
from .oil import Oil
#from .orifice import OrificeTurbulent

def signTrue(x):
    return 1. if x >= 0 else -1.

def sg(x):
    return x if x >= ETQ.Scalar(0.) else ETQ.Scalar(0.)




class ProportionalValve:


    def __init__(self, flowrate_nominal, pressuredrop_tot_nominal=Q.Pressure(70., 'bar'), underlap1=None):
        """
flowrate_nominal:
pressuredrop_tot_nominal:
underlap1:  uv where critical lap

"""
        self.flowrate_nominal = Q.Flowrate(flowrate_nominal)
        self.pressuredrop_tot_nominal = Q.Pressure(pressuredrop_tot_nominal)
        if underlap1:
            self.underlap1 = Q.Scalar(underlap1)
            if not (Q.Scalar(0.0, '1') <= self.underlap1 <= Q.Scalar(1.0, '1')):
                raise Exception('underlap has to be <=1 and >=0')
        else:
            self.underlap1 = Q.Scalar(0.0, '1')

        self.Cq = Q.Scalar(0.67)
        self.fluid = Oil()


    @property
    def Cv1(self):
        """Cv for control signal -1..1"""
        return self.flowrate_nominal / (functions.sqrt(self.pressuredrop_tot_nominal / 2)*(Q.Scalar(1.0, '1') + self.underlap1))

    def param_given_xvmax(self, xvmax):
        xvmax = Q.Distance(xvmax)
        A = Q.Area(self.Cv1 / (self.Cq * functions.sqrt(2./self.fluid.density)))
        dv = Q.Distance(A / (ETQ.PI*xvmax))
        xvunderlap = Q.Distance(xvmax*self.underlap1)
        return {'xvmax':xvmax, 'xvunderlap':xvunderlap, 'spoolDiameter':dv, 'A':A, 'Cq':self.Cq, 'density':self.fluid.density}

    @property
    def pressuredrop1_nominal(self):
        return Q.Pressure(self.pressuredrop_tot_nominal/2)

    def __str__(self):
        return """{name}
Cv1:               {s.Cv1}
underlap1:         {s.underlap1}
Cq:                {s.Cq}
Fluid: {s.fluid}
""".format(name=self.__class__.__module__+'.'+self.__class__.__name__,
           s=self)

    __repr__ = __str__



    def KQxA1_dp(self, dp):
        """Jelali page 105 eq 4.225, simplified"""
        return self.Cv1 * functions.sqrt(dp)


    def KQxB1_dp(self, dp):
        """Jelali page 105 eq 4.226, simplified"""
        return -self.Cv1 * functions.sqrt(dp)


    def KQu(self, position, dp, cylinder):
        """Jelali page 107"""
        # TODO: shall that be pard of valve or cylinder or something else
        return cylinder.fluid.bulkmodulus / cylinder.volume_A(position) * self.KQxA1_dp(dp) - cylinder.fluid.bulkmodulus / cylinder.volume_B(position)* self.KQxB1_dp(dp)


    def Kxdtff(self, position, dp, cylinder):
        """# Jelali page 232 eq 6.48"""
        return cylinder.areaA / (1.0*self.KQu(position, dp, cylinder))*(cylinder.fluid.bulkmodulus / cylinder.volume_A(position) + cylinder.fluid.bulkmodulus/cylinder.volume_B(position))



    def KQxL1__Jelali_4_232(self, xV , pS, pT, pL):
        """Jelali page 106 eq 4.232"""
        return self.Cv1 * np.sqrt(2.) * functions.sqrt(pS - pT - pL* signTrue(xV))


    def KQpL1__Jelali_4_233(self, xV0, xV, pS, pT, pL0):
        """Jelali page 106 eq 4.233
        TODO: whats about the ..0 ?
        """
        return -signTrue(xV) * self.Cv1 * xV0  / (np.sqrt(2.) * functions.sqrt(pS - pT - pL0 * np.sign(xV)))


    def KQxA1__Jelali_4_225(self, xV , pS, pT, pA0, pB0):
        """Flow Gain
        Jelali page 105 eq 4.225"""
        if xV >= ETQ.Scalar(0.,'1'):
            return self.Cv1 * functions.sqrt(pS - pA0)
        else:
            return self.Cv1 * functions.sqrt(pA0 - pT)


    def KQxB1__Jelali_4_226(self, xV , pS, pT, pA0, pB0):
        """Flow Gain
        Jelali page 105 eq 4.226"""
        if xV >= ETQ.Scalar(0.,'1'):
            return - self.Cv1 * functions.sqrt(pB0 - pT)
        else:
            return - self.Cv1 * functions.sqrt(pS - pB0)


    def KQpA1__Jelali_4_227(self, xV , xV0, pS, pT, pA0, pB0):
        if xV >= ETQ.Scalar(0.,'1'):
            return self.Cv1 * xV0 / (2.* functions.sqrt(pA0 - pT))
        else:
            return -self.Cv1 * xV0 / (2.* functions.sqrt(pS - pA0))



    def KQpB1__Jelali_4_228(self, xV , xV0, pS, pT, pA0, pB0):
        if xV >= ETQ.Scalar(0.,'1'):
            return -self.Cv1 * xV0 / (2.* functions.sqrt(pB0 - pT))
        else:
            return self.Cv1 * xV0 / (2.* functions.sqrt(pS - pB0))


    def flow(self, xVn, pA=None, pB=None, pL=None, pS=None, pT=None):
        """
        Jelali page 59 eq 4.2, 4.3
        assumption: all Cv are equal

        xVn ... spool position -1..1

        >>> valve = ProportionalValve(flowrate_nominal=ETQ.Flowrate(20, 'Liter/min'), pressuredrop_tot_nominal=ETQ.Pressure(70, 'bar'), underlap1=0.1)
        >>> QA, QB = valve.flow(0., pL=ETQ.Pressure(0.,'bar'), pS=ETQ.Pressure(70.,'bar'), pT=ETQ.Pressure(0.,'bar'))
        >>> print(QA)
           0     Liter/min (Flowrate)
        >>> print(QB)
           0     Liter/min (Flowrate)
        >>> QA, QB = valve.flow(0.1, pL=ETQ.Pressure(0.,'bar'), pS=ETQ.Pressure(70.,'bar'), pT=ETQ.Pressure(0.,'bar'))
        >>> print(QA)
           3.64  Liter/min (Flowrate)
        >>> print(QB)
          -3.64  Liter/min (Flowrate)
        >>> QA, QB = valve.flow(-0.1, pL=ETQ.Pressure(0.,'bar'), pS=ETQ.Pressure(70.,'bar'), pT=ETQ.Pressure(0.,'bar'))
        >>> print(QA)
          -3.64  Liter/min (Flowrate)
        >>> print(QB)
           3.64  Liter/min (Flowrate)
        """
        xVn = ETQ.Scalar(xVn)
        xVn = functions.limitTo(xVn, ETQ.Scalar(-1.), ETQ.Scalar(1.))
        if pL and (pA is None and pB is None):
            pA = ETQ.Pressure((pS + pT)/2 + pL/2)
            pB = ETQ.Pressure((pS + pT)/2 - pL/2)
            ETQ.logging.info("pA={} pB={}".format(pA, pB))
        Q1 = ETQ.Flowrate(self.Cv1*sg( xVn + self.underlap1)*functions.sqrtSigned(pS-pA))
        Q2 = ETQ.Flowrate(self.Cv1*sg(-xVn + self.underlap1)*functions.sqrtSigned(pA-pT))
        Q3 = ETQ.Flowrate(self.Cv1*sg(-xVn + self.underlap1)*functions.sqrtSigned(pS-pB))
        Q4 = ETQ.Flowrate(self.Cv1*sg( xVn + self.underlap1)*functions.sqrtSigned(pB-pT))
        QA = Q1 - Q2
        QB = Q3 - Q4
        return QA, QB #, (Q1, Q2, Q3, Q4)

# eof

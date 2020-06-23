#!/usr/bin/env python3
# pylint: disable-msg=line-too-long,missing-module-docstring,missing-function-docstring,missing-class-docstring,no-else-return,invalid-name,multiple-statements

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"


from .. import quantities as ETQ
from EngineeringTools.tools import functions
from ..container import Obj

try:
    import control as pc
except ImportError:
    pc = None


class HydraulicServoSystem__Jelali_4_(Obj):

    def __init__(self, valve, cylinder):

        self.valve = valve
        self.cylinder = cylinder
        self.fluid = cylinder.fluid


    def dpA__Jelali_4_236(self, dpL):
        '''Jelali page 107 eq 4.236'''
        return ETQ.Pressure(1./(1. + self.cylinder.areaRatio**3) * dpL)


    def dpB__Jelali_4_237(self, dpL):
        '''Jelali page 107 eq 4.237'''
        return ETQ.Pressure(- self.cylinder.areaRatio**2/(1. + self.cylinder.areaRatio**3) * dpL)


    def KQ__Jelali_4_240(self, xP, xV , pS, pT, pA0, pB0):
        """Jelali page 107 eq 4.240"""
        return                         (self.fluid.bulkmodulus / self.cylinder.volume_A(xP) * self.valve.KQxA1__Jelali_4_225(xV , pS, pT, pA0, pB0)
            - self.cylinder.areaRatio * self.fluid.bulkmodulus / self.cylinder.volume_B(xP) * self.valve.KQxB1__Jelali_4_226(xV , pS, pT, pA0, pB0))


    def Ch__Jelali_4_241(self, xP):
        return (self.fluid.bulkmodulus / self.cylinder.volume_A(xP)
                + self.cylinder.areaRatio**2 * self.fluid.bulkmodulus / self.cylinder.volume_B(xP))


    def Kd__Jelali_4_241(self, xP):
        return self.cylinder.areaA / self.Ch__Jelali_4_241(xP)



    def Th__Jelali_4_242(self, xP, xV , xV0, pS, pT, pA0, pB0):
        ''' CLi = 0'''
        a = self.cylinder.areaRatio
        return 1. / (a*self.fluid.bulkmodulus / self.cylinder.volume_B(xP) * (self.valve.KQpB1__Jelali_4_228(xV , xV0, pS, pT, pA0, pB0) / (ETQ.Scalar(1., '1').uval + a**3))
                     - self.fluid.bulkmodulus / self.cylinder.volume_A(xP) * (self.valve.KQpA1__Jelali_4_227(xV , xV0, pS, pT, pA0, pB0) / (ETQ.Scalar(1., '1').uval + a**3)))



    def omegah__Jelali_4_247(self, xP, mass):
        return ETQ.VelocityAngular(functions.sqrt(self.cylinder.areaP**2 / mass *
                          ( self.fluid.bulkmodulus / self.cylinder.volume_A(xP) +
                            self.cylinder.areaRatio**2 * self.fluid.bulkmodulus / self.cylinder.volume_B(xP) )))

    def Dh__Jelali_4_248(self, xP, xV , pS, pT, pA0, pB0, mass):
        a = self.cylinder.areaRatio
        return 1./ (2.*a/(ETQ.Scalar(1., '1').uval+a**3) * (-a**2*self.fluid.bulkmodulus / self.cylinder.volume_B(xP) * self.valve.KQpB1__Jelali_4_228(xV , xV, pS, pT, pA0, pB0)
                    - self.fluid.bulkmodulus / self.cylinder.volume_A(xP) * self.valve.KQpA1__Jelali_4_227(xV , xV, pS, pT, pA0, pB0))* self.omegah__Jelali_4_247(xP, mass))


    def G_KQ(self,xP, xV , pS, pT, pA0, pB0):
        return pc.tf([self.KQ__Jelali_4_240(xP, xV , pS, pT, pA0, pB0).get_value() ], [1])



    def G_a_xV(self, xP, xV , pS, pT, pA0, pB0, mass):
        return pc.tf(self.cylinder.areaA / mass * [self.KQ__Jelali_4_240(xP, xV , pS, pT, pA0, pB0)])


    def G_xV_vV(self, xP, xV, pS, pT, pA0, pB0, mass):
        Dh = self.Dh__Jelali_4_242(xP, xV, pS, pT, pA0, pB0, mass)
        omegah = self.omegah(xP, mass)
        return pc.tf([1.], [1., 2.*Dh*omegah, omegah**2])




class HydraulicServoSystemSymmetric(Obj):

    def __init__(self, valve, cylinder):
        self.valve = valve
        self.cylinder = cylinder
        self.fluid = cylinder.fluid

    def KQ(self):
        pass

# eof

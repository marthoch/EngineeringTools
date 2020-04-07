#!/usr/bin/env python3
# pylint: disable-msg=line-too-long,missing-module-docstring,missing-function-docstring,missing-class-docstring,no-else-return,invalid-name,multiple-statements

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"

from .. import quantities as Q # depricated
from .. import quantities as ETQ
from ..tools import geo_circle
from EngineeringTools.tools import functions
from .oil import Oil


class Cylinder:
    def __init__(self, D=None, stroke_length=None, stroke_range=None, dA=0.0, dB=0.0, V0=None, V0A=None, V0B=None, A=None, AA=None, AB=None, kind=None, name=None, nominalPressure=None):
        self.kind = kind
        self.name = name
        self.pistion_diameter = D
        self.rod_diameter_A = dA
        self.rod_diameter_B = dB
        self.fluid = Oil()

        if stroke_range:
            if stroke_length:
                raise Exception('specify stroke_length or stroke_range')
            self.position_lowerLimit = Q.Distance(stroke_range[0])
            self.position_upperLimit = Q.Distance(stroke_range[1])
            self.stroke_length = self.position_upperLimit - self.position_lowerLimit
        elif stroke_length:
            self.stroke_length = stroke_length
            self.position_lowerLimit = Q.Distance(-self.stroke_length.uval / 2.)
            self.position_upperLimit = Q.Distance(self.stroke_length.uval / 2.)
        if not (self.position_lowerLimit < self.position_upperLimit):  # pylint: disable=unneeded-not
            raise Exception('lower stroke limit must be smaller as the upper')

        if nominalPressure:
            self._nominalPressure = Q.Pressure(nominalPressure)
        else:
            self._nominalPressure = None

        if A:
            rA = geo_circle.Circle(d=self.rod_diameter_A)
            c = geo_circle.Circle(A=A + rA.area)
            self.pistion_diameter = c.diameter
        # self.fluid_bulkmodulus = Q.Stress(1.5e9, 'Pa') # watton2009_FundamentalsFluidPowerControl page 41

        if V0A:
            self.volumeA_0 = Q.Volume(V0A)
        else:
            if V0:
                self.volumeA_0 = Q.Volume(V0)
            else:
                self.volumeA_0 = Q.Volume(self.areaA * (-self.position_lowerLimit), displayUnit='cm3') # pylint: disable=invalid-unary-operand-type
        if V0B:
            self.volumeB_0 = Q.Volume(V0B)
        else:
            if V0:
                self.volumeB_0 = Q.Volume(V0)
            else:
                self.volumeB_0 = Q.Volume(self.areaA * self.position_upperLimit, displayUnit='cm3')

    def __repr__(self):
        return """Cylinder:
kind                    {S.kind}
stroke length         = {stroke_length}
stroke range          = [{S.position_lowerLimit} {S.position_upperLimit}]
piston diameter       = {pistion_diameter}
piston rod diameter A = {rod_diameter_A}
piston rod diameter B = {rod_diameter_B}
dead volume A         = {volumeA_0}
dead volume B         = {volumeB_0}
piston area A         = {pistonAreaA}
piston area B         = {pistonAreaB}
{fluid}
        """.format(S=self,
                   stroke_length=self.stroke_length,
                   pistion_diameter=self.pistion_diameter,
                   rod_diameter_A=self.rod_diameter_A,
                   rod_diameter_B=self.rod_diameter_B,
                   volumeA_0=self.volumeA_0,
                   volumeB_0=self.volumeB_0,
                   pistonAreaA=self.areaA,
                   pistonAreaB=self.areaB,
                   fluid=self.fluid)

    def validPosition(self, position):
        position = Q.Distance(position)
        if not (self.position_lowerLimit <= position <= self.position_upperLimit):
            raise Exception('position is out of range')
        return position

    @property
    def areaA(self):
        return Q.Area((self.pistion_diameter.uval**2 - self.rod_diameter_A.uval**2) * Q.PI/4.)

    @property
    def areaB(self):
        return Q.Area((self.pistion_diameter.uval**2 - self.rod_diameter_B.uval**2) * Q.PI/4.)

    areaP = areaA

    @property
    def areaRatio(self):
        return Q.Scalar(self.areaA / self.areaB)


    def force(self, pA, pB):
        return Q.Force(self.areaA * pA - self.areaB * pB)

    @property
    def nominalPressure(self):
        return self._nominalPressure

    @nominalPressure.setter
    def nominalPressure(self, nominalPressure):
        self._nominalPressure = Q.Pressure(nominalPressure)

    @property
    def forceNominal(self):
        return {'A':self.force(pA=self.nominalPressure, pB=Q.Pressure(0.,'bar')), 'B':self.force(pA=Q.Pressure(0.,'bar'), pB=self.nominalPressure)  }

    def stiffness(self, position):
        position = Q.Distance(position)
        VA = self.volume_A(position)
        CA = self.fluid.bulkmodulus  * self.areaA**2 / VA
        VB = self.volume_B(position)
        CB = self.fluid.bulkmodulus  * self.areaB**2 / VB
        C = CA + CB # parallel
        return C


    def volume_A(self, position):
        position = self.validPosition(position)
        return Q.Volume(self.volumeA_0.uval + self.areaA * position)


    def volume_B(self, position):
        position = self.validPosition(position)
        return Q.Volume(self.volumeB_0.uval - self.areaB * position)


    def capacitanceA(self, position):
        return self.volume_A(position) / self.fluid.bulkmodulus


    def capacitanceB(self, position):
        return self.volume_B(position) / self.fluid.bulkmodulus


    def naturalFrequency(self, position, mass):
        mass = Q.Mass(mass)
        position = self.validPosition(position)
        kh = self.stiffness(position)
        return Q.Frequency(functions.sqrt(kh / mass) * 1. / (2.* Q.PI))

    def naturalFrequency_plot(self, mass):
        pass
# EOF

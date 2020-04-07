#!/usr/bin/env python3
# pylint: disable-msg=line-too-long,missing-module-docstring,missing-function-docstring,missing-class-docstring,no-else-return,invalid-name,multiple-statements

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"


import copy
import numpy as np

from .. import quantities as Q
from EngineeringTools.tools import functions
from .oil import Oil


class OrificeTurbulent:


    def __init__(self, A=None, pressure_drop=None, p1=None, p2=None, flow=None, fluid=None, Cq=None):
        self.A = None
        if Cq:
            self.Cq = Cq
        else:
            self.Cq = Q.Scalar(0.67)
        if fluid:
            self.fluid = fluid
        else:
            self.fluid = Oil()

        if A:
            self.A = A
        elif (pressure_drop is not None and flow is not None and A is None and p1 is None and p2 is None):
            self.A = Q.Area(flow.uval / self.Cq.uval  / functions.sqrt(2./self.fluid.density.uval * abs(pressure_drop.uval)))
        elif A is None and p1 is not None  and p2 is not None  and flow is not None:
            pressure_drop = p1 - p2
            self.A = Q.Area(flow.uval / self.Cq.uval  / functions.sqrt(2./self.fluid.density.uval * abs(pressure_drop.uval)))

    def copy(self):
        return copy.copy(self)

    def flow(self, p1=None, p2=None, pressure_drop=None):
        if (p1 is not None)  and (p2 is not None) and (pressure_drop is None):
            pressure_drop = p1 - p2
        return Q.Flowrate(np.sign(pressure_drop.value) * self.Cq * self.A * functions.sqrt(2./self.fluid.density * abs((pressure_drop).uval)))

    def pressure_drop(self, flow):
        return  Q.Pressure(np.sign(flow.value) * (flow / (self.Cq * self.A))**2 / 2. * self.fluid.density)

    def __str__(self):
        return """{name}
Cq:                {Cq}
A:                 {A}  
Fluid: {fluid}
""".format(name=self.__class__.__module__+'.'+self.__class__.__name__,
           Cq=self.Cq,
           A=self.A,
           fluid=self.fluid)

    __repr__ = __str__

#eof

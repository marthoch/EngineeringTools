#!/usr/bin/env python3
# pylint: disable-msg=line-too-long,missing-module-docstring,missing-function-docstring,missing-class-docstring,no-else-return,invalid-name,multiple-statements

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"

from .. import quantities as Q
from .. import quantities as ETQ
from EngineeringTools.tools import functions

class Oil:

    def __init__(self):
        self.description = 'general hydraulic oil'
        self.bulkmodulus = Q.Stress(1.0e9, 'Pa')
        self.density = Q.Density(890., 'kg/m^3')


    def _repr_html_(self):
        html = """<font face="courier">
{name}        
<table border="1">
<tr>
<td>description</td>
<td>{s.description}</td>
</tr>
<tr>
<td>density</td>
<td>{s.density}</td>
</tr>
<tr>
<td>bulk modulus</td>
<td>{s.bulkmodulus}</td>
</tr>
</table>
</font>
""".format(name=self.__class__.__module__+'.'+self.__class__.__name__, s=self)
        return html

    def __str__(self):
        return """{name}
description:       {s.description}    
density:           {s.density}  
bulk modulus:      {s.bulkmodulus}
""".format(name=self.__class__.__module__+'.'+self.__class__.__name__,
           s=self)

    __repr__ = __str__



class Oil_ShellTellusS2M46(Oil):

    def __init__(self):
        super(Oil_ShellTellusS2M46, self).__init__()
        self.description = "Shell Tellus S2 M 46"
        self.density = Q.Density(879., 'kg/m^3') # at 15degC from Technical Data Sheet 2015

        self.viscosityKinematic_tab = [[Q.TemperatureAbsolute(  0.,'degC'), Q.ViscosityKinematic(580., 'cSt')],
                                       [Q.TemperatureAbsolute( 40.,'degC'), Q.ViscosityKinematic(46., 'cSt')],
                                       [Q.TemperatureAbsolute(100.,'degC'), Q.ViscosityKinematic(6.7, 'cSt')]]

    def viscosityKinematic(self, temperatur):

        temp = []
        visc = []
        for t, v in  self.viscosityKinematic_tab:
            temp.append(t.get_value())
            visc.append(v.get_value())

        x = temp
        y = visc
        log = functions.log
        k0 = (x[0]*x[1]*(x[0] - x[1])*log(y[2]) - x[0]*x[2]*(x[0] - x[2])*log(y[1]) + x[1]*x[2]*(x[1] - x[2])*log(y[0]))/(x[0]**2*x[1] - x[0]**2*x[2] - x[0]*x[1]**2 + x[0]*x[2]**2 + x[1]**2*x[2] - x[1]*x[2]**2)
        k1 = (-(x[0]**2 - x[1]**2)*log(y[2]) + (x[0]**2 - x[2]**2)*log(y[1]) - (x[1]**2 - x[2]**2)*log(y[0]))/(x[0]**2*x[1] - x[0]**2*x[2] - x[0]*x[1]**2 + x[0]*x[2]**2 + x[1]**2*x[2] - x[1]*x[2]**2)
        k2 = ((x[0] - x[1])*log(y[2]) - (x[0] - x[2])*log(y[1]) + (x[1] - x[2])*log(y[0]))/(x[0]**2*x[1] - x[0]**2*x[2] - x[0]*x[1]**2 + x[0]*x[2]**2 + x[1]**2*x[2] - x[1]*x[2]**2)

        return  ETQ.ViscosityKinematic(functions.exp(k0 + k1 *  temperatur.get_value() +  k2 * temperatur.get_value()**2), 'm^2/sec')


    def viscosityDynamic(self, temperatur):
        return ETQ.ViscosityDynamic(self.viscosityKinematic(temperatur) * self.density)


if __name__ == '__main__':
    pass

#eof

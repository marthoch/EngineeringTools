#!/usr/bin/env python3
# pylint: disable=line-too-long,wrong-import-position,abstract-method,no-else-return

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"

import os

#import numpy as np
from numpy import r_
#import scipy as sp
import scipy.stats as spstats
import pandas as pd


from .. import quantities as ETQ
#from ..tools import tools, geo_circle
#from EngineeringTools.mechanics import beamsection
#from ..hydraulics.oil import Oil


class ETP_OCTOPUS_O:
    filename = os.path.join(os.path.dirname(__file__), r'ETP_OCTOPUS_O.txt')


    def __init__(self, id=None, d=None):

        database = pd.read_csv(self.filename, skiprows=3, sep=r'\s*;\s*', index_col=0, engine='python')
        if id:
            dataset = database.loc[id]
        elif d:
            dataset = database[database['d'] == d].iloc[0]
        else:
            raise Exception()
        self.dataset = dataset
        self.name   = dataset.name
        self.length = ETQ.Distance(dataset['L'], 'mm')
        self.B      = ETQ.Distance(dataset['b'], 'mm')
        self.inner_diameter = ETQ.Distance(dataset['d'], 'mm')
        self.outer_diameter = ETQ.Distance(dataset['D'], 'mm')
        self.oil_clearance = ETQ.Distance(dataset['oilClearance'], 'mm')
        self.lst_force = [ETQ.Force(dataset['F1'], 'kN'), ETQ.Force(dataset['F2'], 'kN')]
        self.lst_pressure = [ETQ.Pressure(350., 'bar'), ETQ.Pressure(450., 'bar')]
        self.friction_coefficient_design = 0.1

        self.friction_coefficient = r_[0.05, 0.1, 0.2] # steel on steel, oil: 0.05 .. 0.1, 0.2 without oil
        self.pressure_offset = r_[5.0, 10., 20.]*1e5 # Pa, pressure where clamping starts

        # add the zero point
        # TODO: this is not perfect, more data needed
        self.lst_force.append(ETQ.Force(0., 'N'))
        self.lst_pressure.append(ETQ.Pressure(1., 'bar'))
        self.calc_param()
        del self.lst_force[-1]
        del self.lst_pressure[-1]


    def calc_param(self):
        p = r_[[x.value for x in self.lst_pressure]]
        F = r_[[x.value for x in self.lst_force]]
        slope, intercept, _, _, _ = spstats.linregress(p, F)
        self.active_area = ETQ.Area(slope / self.friction_coefficient_design, 'm2')
        self.p0 = ETQ.Pressure(-intercept / slope, 'Pa')


    def __str__(self):
        pf = ""
        for p, f in zip(self.lst_pressure, self.lst_force):
            pf += '{} {}\n'.format(p, f)
        return """ETP ClampingElement
name:           {me.name}
rod diameter:   {me.inner_diameter}
outer diameter: {me.outer_diameter}
length:         {me.length}
p0:             {me.p0}
{pf}
""".format(me=self,
           pf=pf)

    __repr__ = __str__



    @classmethod
    def list_all(cls):
        database = pd.read_csv(cls.filename, skiprows=3, sep=r'\s*;\s*', index_col=0, engine='python')
        return database #.index()

    def clamp_force(self, pressure):
        pressure = ETQ.Pressure(pressure)
        return ETQ.Force(self.active_area*self.friction_coefficient_design* max(pressure - self.p0, ETQ.Pressure(0.0, 'Pa')))

    def clamp_pressure_needed(self, force):
        force = ETQ.Force(force)
        return ETQ.Pressure(force / (self.active_area*self.friction_coefficient_design)  + self.p0.uval)

#eof

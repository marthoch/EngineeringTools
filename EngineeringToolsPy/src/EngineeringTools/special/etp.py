#!/usr/bin/env python3
# pylint: disable=line-too-long,wrong-import-position,abstract-method,no-else-return
from statsmodels.tsa.tests.test_x13 import dataset
from h5py._hl.dataset import Dataset

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



class ETPHydrHubShaftConnection:
    """
    https://etp.se/sites/default/files_two/ETP-EXPRESS-PRODUCT-SHEET.pdf
    """
    filename = os.path.join(os.path.dirname(__file__), r'ETPHydrHubShaftConnection.txt')

    @classmethod
    def read_database(cls):
        """read the database from the file """
        cls.database = pd.read_csv(cls.filename, skiprows=4, sep=r'\s*;\s*', index_col=0, engine='python')

    @classmethod
    def search(cls, kind=None, d=None, D=None, minT=None):
        datasets = cls.database
        if kind:
            datasets = datasets[datasets['kind'] == kind]
        if d:
            if isinstance(d, ETQ.Distance):
                d = d.get_value('mm')
            datasets = datasets[datasets['d'] == d]
        if D:
            if isinstance(D, ETQ.Distance):
                D = D.get_value('mm')
            datasets = datasets[datasets['D'] == D]
        if minT:
            if isinstance(minT, ETQ.Torque):
                minT = minT.get_value('N.m')
            datasets = datasets[datasets['T'] >= minT]
        return datasets.sort_values( ['d', 'D','L1','m'])


    def __init__(self, name=None, kind=None, d=None, D=None, minT=None):

        if name:
            dataset = self.database.loc[name]
        else:
            datasets = self.search(d=d)
            if len(datasets) == 1:
                dataset = datasets.iloc[0]
            else:
                print(datasets)
                raise Exception('More or less than one products fit the parameters, use search method')
        self.dataset = dataset
        self.name   = dataset.name
        self.length = ETQ.Distance(dataset['L'], 'mm')
        self.lengthTotal = ETQ.Distance(dataset['L1'], 'mm')
        self.inner_diameter = ETQ.Distance(dataset['d'], 'mm')
        self.outer_diameter = ETQ.Distance(dataset['D'], 'mm')
        self.torque = ETQ.Torque(dataset['T'], 'N.m')
#        self.lst_force = [ETQ.Force(dataset['F1'], 'kN'), ETQ.Force(dataset['F2'], 'kN')]
#        self.lst_pressure = [ETQ.Pressure(350., 'bar'), ETQ.Pressure(450., 'bar')]
        self.friction_coefficient_design = 0.1
 
        self.friction_coefficient = r_[0.05, 0.1, 0.2] # steel on steel, oil: 0.05 .. 0.1, 0.2 without oil
#        self.pressure_offset = r_[5.0, 10., 20.]*1e5 # Pa, pressure where clamping starts
 
        # add the zero point
        # TODO: this is not perfect, more data needed
#        self.lst_force.append(ETQ.Force(0., 'N'))
#        self.lst_pressure.append(ETQ.Pressure(1., 'bar'))
#        self.calc_param()
#        del self.lst_force[-1]
#        del self.lst_pressure[-1]


#     def calc_param(self):
#         p = r_[[x.value for x in self.lst_pressure]]
#         F = r_[[x.value for x in self.lst_force]]
#         slope, intercept, _, _, _ = spstats.linregress(p, F)
#         self.active_area = ETQ.Area(slope / self.friction_coefficient_design, 'm2')
#         self.p0 = ETQ.Pressure(-intercept / slope, 'Pa')


    def __str__(self):
#        pf = ""
#        for p, f in zip(self.lst_pressure, self.lst_force):
#            pf += '{} {}\n'.format(p, f)
        return """ETP ClampingElement
name:           ETP_EXPRESS {me.name}
rod diameter:   {me.inner_diameter}
outer diameter: {me.outer_diameter}
length:         {me.length}
lengthTotal:    {me.lengthTotal}
Torque:         {me.torque}
 
""".format(me=self)

    __repr__ = __str__

    @classmethod
    def list_all(cls):
        return cls.database #.index()

#     def clamp_force(self, pressure):
#         pressure = ETQ.Pressure(pressure)
#         return ETQ.Force(self.active_area*self.friction_coefficient_design* max(pressure - self.p0, ETQ.Pressure(0.0, 'Pa')))
# 
#     def clamp_pressure_needed(self, force):
#         force = ETQ.Force(force)
#         return ETQ.Pressure(force / (self.active_area*self.friction_coefficient_design)  + self.p0.uval)

ETPHydrHubShaftConnection.read_database()


#eof

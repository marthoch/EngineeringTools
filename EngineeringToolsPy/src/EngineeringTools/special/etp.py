#!/usr/bin/env python3
# pylint: disable=line-too-long,wrong-import-position,abstract-method,no-else-return
__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"

import os
#import numpy as _np
from numpy import r_
#import scipy as _sp
import scipy.stats as spstats
import pandas as pd

from .. import quantities as ETQ


class ETP_OCTOPUS_O:
    filename = os.path.join(os.path.dirname(__file__), r'ETP_OCTOPUS_O.txt')


    def __init__(self, name=None, d=None):

        database = pd.read_csv(self.filename, skiprows=3, sep=r'\s*;\s*', index_col=0, engine='python')
        if name:
            dataset = database.loc[name]
        elif d:
            dataset = database[database['d'] == d].iloc[0]
        else:
            raise Exception()
        self.dataset = dataset
        self.name   = dataset.name
        self.length = ETQ.Distance(dataset['L'], 'mm')
        self.B      = ETQ.Distance(dataset['b'], 'mm')
        self.diameter_inner = ETQ.Distance(dataset['d'], 'mm')
        self.diameter_outer = ETQ.Distance(dataset['D'], 'mm')
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
        return """ETP_OCTOPUS_O
name:           {me.name}
rod diameter:   {me.diameter_inner}
outer diameter: {me.diameter_outer}
length:         {me.length}
p0:             {me.p0}
{pf}
""".format(me=self,
           pf=pf)

    __repr__ = __str__


    @classmethod
    def list_all(cls):
        database = pd.read_csv(cls.filename, skiprows=3, sep=r'\s*;\s*', index_col=0, engine='python')
        return database

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
        cls.database = pd.read_csv(cls.filename, skiprows=1, sep=r'\s*;\s*', index_col=0, engine='python')

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
            datasets = self.search(kind=kind, d=d, D=D, minT=minT)
            if len(datasets) == 1:
                dataset = datasets.iloc[0]
            else:
                print(datasets)
                raise Exception('More or less than one products fit the parameters, use search method')
        self.dataset = dataset
        self.name_str   = dataset.name
        self.name       = ETQ.String(dataset.name)
        self.length     = ETQ.Distance(dataset['L'], 'mm')
        self.length_total   = ETQ.Distance(dataset['L1'], 'mm')
        self.diameter_inner = ETQ.Distance(dataset['d'], 'mm')
        self.diameter_outer = ETQ.Distance(dataset['D'], 'mm')
        self.torque         = ETQ.Torque(dataset['T'], 'N.m')

    def __str__(self):
        return """ETPHydrHubShaftConnection
name:           {me.name}
rod diameter:   {me.diameter_inner}
outer diameter: {me.diameter_outer}
length:         {me.length}
length total:   {me.length_total}
torque:         {me.torque}
 
""".format(me=self)

    __repr__ = __str__


    def _repr_html_(self):
        html = """ETPHydrHubShaftConnection<br>
<table border="1">\n"""
        def oneline(k, v):
            return """<tr>
<td>{:s}</td>
<td style="text-align:left">{:s}</td>
</tr>
""".format(k, v._repr_html_())
        html += oneline('name', self.name)
        html += oneline('rod diameter', self.diameter_inner)
        html += oneline('outer diameter', self.diameter_outer)
        html += oneline('length', self.length)
        html += oneline('length total', self.length_total)
        html += oneline('torque', self.torque)
        html += """</table>
</font>\n"""
        return html

    @classmethod
    def list_all(cls):
        """Return a list of all Hub-Shaft Connections
        """
        return cls.database.copy()


ETPHydrHubShaftConnection.read_database()

#eof
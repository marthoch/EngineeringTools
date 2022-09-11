#!/usr/bin/env python3
# pylint: disable-msg=line-too-long,missing-module-docstring,missing-function-docstring,missing-class-docstring,no-else-return,invalid-name
"""
Read Trace files (.csv) from Atlas Copco ToolsTalk2

https://github.com/marthoch/EngineeringTools/blob/master/EngineeringToolsPy/src/EngineeringTools/other/AtlasCopco_TraceFile.py
"""
__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"

import logging
import datetime
import scipy as sp
import scipy.signal as spsig
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class ToolsTrace():

    def __init__(self, filename, direction=None, traceName=None):
        self.filename = filename
        self.traceName = traceName
        if direction in ('CW', 'CCW', None):
            self.direction = direction
        else:
            logging.error('direction must be "CW", "CCW", or None (== CW) but was "{}"'.format(direction))
        self._read_file()

    def _read_file(self):
        logging.info('reading file "{}"'.format(self.filename))
        filepos = {}
        with open(self.filename, 'rt', encoding="ascii", newline='\r\n') as f:
            txt = f.readlines()
            txt = [t.rstrip() for t in txt]
            filepos['Torque Measurement Points'] = txt.index('Torque Measurement Points') + 1
            filepos['Angle Measurement Points'] = txt.index('Angle Measurement Points') + 1
            filepos['Trace Points'] = txt.index('Trace Points') + 1
            filepos['StepResult'] = txt.index('StepResult') + 1
            filepos['Angle Measurement Points: length'] = filepos['Trace Points'] - filepos['Angle Measurement Points'] - 3
            filepos['Torque Measurement Points: length'] = filepos['Angle Measurement Points'] - filepos['Torque Measurement Points'] - 3
            filepos['Trace Points: length'] = filepos['StepResult'] - filepos['Trace Points'] - 3
            filepos['StepResult: length'] =  len(txt) - filepos['StepResult'] - 1 +1
            #filepos['len'] =  len(txt)
        logging.debug(filepos)
        #self.filepos = filepos

        self.df_Task = pd.read_csv(self.filename, header=1, nrows=1)
        self.df_TraceConversion = pd.read_csv(self.filename, header=4, nrows=1)

        self.df_TorqueMeasurementPoints = pd.read_csv(self.filename, header=filepos['Torque Measurement Points'], nrows=filepos['Torque Measurement Points: length'], engine='python', encoding="ascii", skip_blank_lines=False)
        self.df_TorqueMeasurementPoints.set_index('Name', inplace=True)

        self.df_AngleMeasurementPoints = pd.read_csv(self.filename, header=filepos['Angle Measurement Points'], nrows=filepos['Angle Measurement Points: length'], engine='python', encoding="ascii", skip_blank_lines=False)
        self.df_AngleMeasurementPoints.set_index('Name', inplace=True)

        if filepos['StepResult: length'] > 0:
            self.df_StepResult = pd.read_csv(self.filename, header=filepos['StepResult'], nrows=filepos['StepResult: length'], engine='python', encoding="ascii", skip_blank_lines=False)
            self.df_StepResult.rename(str.strip, axis='columns', inplace=True)
            self.df_StepResult.set_index('StepNumber', inplace=True)
        else:
            self.df_StepResult = None

        self.df_TracePointsRaw = pd.read_csv(self.filename, header=filepos['Trace Points'], nrows=filepos['Trace Points: length'], engine='python', encoding="ascii", skip_blank_lines=False)
        self.raw_AngleConversionFactor = self.df_TraceConversion['Angle Conversion Factor'][0]
        self.raw_TorqueConversionFactor = self.df_TraceConversion['Torque Conversion Factor'][0]
        if self.direction == 'CCW':
            self.raw_TorqueConversionFactor *= -1.
        self.raw_TraceTimePerSample = self.df_TraceConversion['Trace Time per Sample'][0]
        self.df_TracePoints = pd.DataFrame()
        self.df_TracePoints['Angle Min in deg'] = self.df_TracePointsRaw['Angle Min'] * self.raw_AngleConversionFactor 
        self.df_TracePoints['Angle Max in deg'] = self.df_TracePointsRaw['Angle Max'] * self.raw_AngleConversionFactor
        self.df_TracePoints['Angle Median in deg'] = (self.df_TracePoints['Angle Min in deg'] + self.df_TracePoints['Angle Max in deg']) / 2
        self.df_TracePoints['Angle Median in rot'] = self.df_TracePoints['Angle Median in deg'] / 360
        self.df_TracePoints['Torque Min in Nm'] = self.df_TracePointsRaw['Torque Min'] * self.raw_TorqueConversionFactor
        self.df_TracePoints['Torque Max in Nm'] = self.df_TracePointsRaw['Torque Max'] * self.raw_TorqueConversionFactor
        self.df_TracePoints['Torque Median in Nm'] = (self.df_TracePoints['Torque Min in Nm'] + self.df_TracePoints['Torque Max in Nm']) / 2
        self.df_TracePoints['Time in s'] = self.df_TracePoints.index * self.raw_TraceTimePerSample
        self.df_TracePoints.set_index('Time in s', inplace=True)

        s = self.df_TracePoints['Angle Median in rot'].diff(1) / self.raw_TraceTimePerSample
        s = spsig.medfilt(s)
        self.df_TracePoints['Angular Speed in rot/s'] = s

    @property
    def VirtualStationName(self):
        return self.df_Task['VirtualStationName'][0]

    @property
    def TaskName(self):
        return self.df_Task['TaskName'][0]

    @property
    def Status(self):
        return self.df_Task['Status'][0]

    @property
    def DateTime(self):
        return datetime.datetime.strptime(self.df_Task['DateTime'][0], '%m/%d/%Y %I:%M:%S %p')

    @property
    def ResultOk(self):
        return self.df_Task['ResultOk'][0]

    @property
    def TracePoints(self):
        return self.df_TracePoints

    @property
    def AngleMeasurementPoints(self):
        return self.df_AngleMeasurementPoints

    @property
    def TorqueMeasurementPoints(self):
        return self.df_TorqueMeasurementPoints    

    def __str__(self):
        return """ToolsTrace(filename='{s.filename}')
    Title              = '{title}'
    VirtualStationName = '{s.VirtualStationName}'
    TaskName           = '{s.TaskName}'
    Status / ResultOk  = {s.Status} / {s.ResultOk}
    DateTime           = {s.DateTime}""".format(s=self, title=self.title())
    
    __repr__ = __str__

    def title(self):
        if self.traceName:
            return self.traceName
        else:
            return '{self.TaskName} {self.DateTime}'.format(self=self)

    def save2matlab(self, filename=None, print_help=False):
        if filename is None:
            filename = self.filename + '.mat'
        df = self.df_TracePoints.copy()
        df = df.reset_index()
        df.rename(columns=lambda x: x.replace(' ', '_'), inplace=True)
        dataML = {'TracePoints': df.to_dict("list")}
        dataML['Task'] = self.df_Task.to_dict()
        dataML['AngleMeasurementPoints'] = self.df_AngleMeasurementPoints.to_dict()
        dataML['TorqueMeasurementPoints'] = self.df_TorqueMeasurementPoints.to_dict()
        scipy.io.savemat(filename, dataML)
        logging.info('saved data to :' + filename)

        if print_help:
            print("""matlab:
t = load('{}')
plot(t.TracePoints.Angle_Median_in_rot, t.TracePoints.Torque_Median_in_Nm)
""".format(filename))

    def _TorqueMeasurementPointsWC(self):
        chained_assignment = pd.get_option('mode.chained_assignment')
        pd.set_option('mode.chained_assignment', None)
        TMP = self.TorqueMeasurementPoints.copy()
        TMP['color'] = None
        for i in TMP.index:
            if i.startswith('mp_'):
                TMP['color'][i] = 'blue'
            elif i.startswith('tgt_'):
                TMP['color'][i] = 'green'
            elif i.startswith('lim_'):
                TMP['color'][i] = 'red'
        pd.set_option('mode.chained_assignment', chained_assignment)
        return TMP

    def plot_trace(self, fig=None, synchPeak=None, **plotparameter):
        if fig:
            axs = fig.axes
        else:
            fig, axs = plt.subplots(3, 1, sharex=True)
        #fig.suptitle('{self.TaskName} {self.DateTime}'.format(self=self))

        fig.canvas.manager.set_window_title('{} Trace Plot'.format(self.title()))

        TMP = self._TorqueMeasurementPointsWC()

        # calc synchronization
        time0 = 0.0
        selftrace = self.TracePoints.copy()
        if synchPeak is True:
            tT = selftrace['Torque Median in Nm']
            if tT.max() > -0.5 * tT.min():
                synchi = tT.to_numpy().argmax()
            else:
                synchi = tT.to_numpy().argmin()
            time0 = selftrace.index[synchi]
            selftrace.index -= time0
            selftrace['Angle Median in rot'] -= selftrace['Angle Median in rot'].iloc[synchi]

        if 'label' in plotparameter:
            label = plotparameter['label']
            plotparameter.pop('label')
        else:
            label = self.title()

        # plot speed
        ax = selftrace.plot(ax=axs[0], y='Angular Speed in rot/s', label=label, **plotparameter)
        ax.set_ylabel('Angular Speed in rot/s')

        # plot angle
        ax = selftrace.plot(ax=axs[1], y='Angle Median in rot', label=label, **plotparameter)
        ax.set_ylabel('Angle Median in rot')
        for i in self.TorqueMeasurementPoints[self.TorqueMeasurementPoints['Angle'] != 0.0].index:
            a = self.TorqueMeasurementPoints['Angle'][i] / 360
            c = TMP['color'][i]
            ax.axhline(y=a, alpha=0.3, color=c)

        # plot torque
        ax = selftrace.plot(ax=axs[2], y='Torque Median in Nm', label=label, **plotparameter)
        ax.set_ylabel('Torque Median in Nm')
        for i in self.TorqueMeasurementPoints[self.TorqueMeasurementPoints['Torque'] != 0.0].index:
            T = self.TorqueMeasurementPoints['Torque'][i]
            c = TMP['color'][i]
            ax.axhline(y=T, alpha=0.3, color=c)

        for ax in axs:
            ax.grid(True, which='both')
            ax.legend().set_visible(False)
#            for t in self.TorqueMeasurementPoints[self.TorqueMeasurementPoints['Time'] != 0.0]['Time']:
            for t in self.TorqueMeasurementPoints['Time']:
                ax.axvline(x=t-time0, alpha=0.2, color='red')
            if self.df_StepResult is not None:
                for index, row in self.df_StepResult.iterrows():
                    t = row['StartTime']
                    ax.axvline(x=t-time0, alpha=0.2, color='red')

        fig.set_size_inches(np.r_[250, 250 / 1.4] / 25.4)
        fig.tight_layout(pad=3, w_pad=1.0, h_pad=1.0)
        return fig


    def plot_trace_angle(self, fig=None, angleOffsetDeg=None, synchPeak=None, **plotparameter):
        if fig:
            ax = fig.axes[0]
        else:
            fig, ax = plt.subplots(1, 1)
        fig.canvas.manager.set_window_title('{} Trace Angle Plot'.format(self.title()))

        selftrace = self.TracePoints.copy()
        if synchPeak is True:
            tT = self.TracePoints['Torque Median in Nm']
            if tT.max() > -0.5*tT.min():
                angleOffsetDeg = - self.TracePoints['Angle Median in deg'].iloc[tT.to_numpy().argmax()]
            else:
                angleOffsetDeg = - self.TracePoints['Angle Median in deg'].iloc[tT.to_numpy().argmin()]
        if angleOffsetDeg is None:
            angleOffsetDeg = -self.TracePoints['Angle Median in deg'].max()

        selftrace['Angle0 Median in deg'] = self.TracePoints['Angle Median in deg'] + angleOffsetDeg

        if 'label' in plotparameter:
            label = plotparameter['label']
            plotparameter.pop('label')
        else:
            label = self.title()
        selftrace.plot(ax=ax, x='Angle0 Median in deg', y='Torque Median in Nm', label=label, **plotparameter)
        ax.grid(True, which='both')
        ax.set_ylabel('Torque Median in Nm')
        ax.legend().set_visible(False)

        TMP = self._TorqueMeasurementPointsWC()

        for i in self.TorqueMeasurementPoints[self.TorqueMeasurementPoints['Angle'] != 0.0].index:
            a = self.TorqueMeasurementPoints['Angle'][i] + angleOffsetDeg
            c = TMP['color'][i]
            ax.axvline(x=a, alpha=0.3, color=c)

        for i in self.TorqueMeasurementPoints[self.TorqueMeasurementPoints['Torque'] != 0.0].index:
            T = self.TorqueMeasurementPoints['Torque'][i]
            c = TMP['color'][i]
            ax.axhline(y=T, alpha=0.3, color=c)

        if self.df_StepResult is not None:
            for index, row in self.df_StepResult.iterrows():
                dp = self.df_TracePoints.iloc[self.df_TracePoints.index.get_loc(row['StartTime'], method='nearest')]
                a = dp['Angle Median in deg'] + angleOffsetDeg
                ax.axvline(x=a, alpha=0.2, color='red')
                ax.axhline(y=dp['Torque Median in Nm'], alpha=0.2, color='red')

        fig.set_size_inches(np.r_[250, 250 / 1.4] / 25.4)
        fig.tight_layout(pad=3, w_pad=1.0, h_pad=1.0)

        return fig

# eof
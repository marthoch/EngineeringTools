import logging
import scipy as sp
import scipy.signal as spsig
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class ToolsTrace():
    
    def __init__(self, filename):
        self.filename = filename
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
            filepos['StepResult: length'] =  len(txt) - filepos['StepResult'] - 1
            #filepos['len'] =  len(txt)
        logging.debug(filepos)
        #self.filepos = filepos
        
        self.df_Task = pd.read_csv(self.filename, header=1, nrows=1)
        self.df_TraceConversion = pd.read_csv(self.filename, header=4, nrows=1)

        self.df_TorqueMeasurementPoints = pd.read_csv(self.filename, header=filepos['Torque Measurement Points'], nrows=filepos['Torque Measurement Points: length'], engine='python', encoding="ascii", skip_blank_lines=False)
        self.df_TorqueMeasurementPoints.set_index('Name', inplace=True)
        
        self.df_AngleMeasurementPoints = pd.read_csv(self.filename, header=filepos['Angle Measurement Points'], nrows=filepos['Angle Measurement Points: length'], engine='python', encoding="ascii", skip_blank_lines=False)
        self.df_AngleMeasurementPoints.set_index('Name', inplace=True)
        
        self.df_StepResult = pd.read_csv(self.filename, header=filepos['StepResult'], nrows=filepos['StepResult: length'], engine='python', encoding="ascii", skip_blank_lines=False)
        self.df_StepResult.rename(str.strip, axis='columns', inplace=True)
        self.df_StepResult.set_index('StepNumber', inplace=True)
        
        
        self.df_TracePointsRaw = pd.read_csv(self.filename, header=filepos['Trace Points'], nrows=filepos['Trace Points: length'], engine='python', encoding="ascii", skip_blank_lines=False)
        self.raw_AngleConversionFactor = self.df_TraceConversion['Angle Conversion Factor'][0]
        self.raw_TorqueConversionFactor = self.df_TraceConversion['Torque Conversion Factor'][0]
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
        return self.df_Task['DateTime'][0]
    
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
    VirtualStationName = '{s.VirtualStationName}'
    TaskName           = '{s.TaskName}'
    Status / ResultOk  = {s.Status} / {s.ResultOk}
    DateTime           = {s.DateTime}""".format(s=self)
    
    __repr__ = __str__

    def title(self):
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
    
    def plot_trace(self, fig=None):
        if fig:
            axs = fig.axes
        else:
            fig, axs = plt.subplots(3, 1, sharex=True)
        #fig.suptitle('{self.TaskName} {self.DateTime}'.format(self=self))

        fig.canvas.set_window_title('{} Trace Plot'.format(self.title()))

        TMP = self._TorqueMeasurementPointsWC()

        ax = self.TracePoints.plot(ax=axs[0], y='Angular Speed in rot/s', label=self.title())
        ax.set_ylabel('Angular Speed in rot/s')

        ax = self.TracePoints.plot(ax=axs[1], y='Angle Median in rot', label=self.title())
        ax.set_ylabel('Angle Median in rot')
        for i in self.TorqueMeasurementPoints[self.TorqueMeasurementPoints['Angle'] != 0.0].index:
            a = self.TorqueMeasurementPoints['Angle'][i] / 360
            c = TMP['color'][i]
            ax.axhline(y=a, alpha=0.3, color=c)

        ax = self.TracePoints.plot(ax=axs[2], y='Torque Median in Nm', label=self.title())
        ax.set_ylabel('Torque Median in Nm')
        for i in self.TorqueMeasurementPoints[self.TorqueMeasurementPoints['Torque'] != 0.0].index:
            T = self.TorqueMeasurementPoints['Torque'][i]
            c = TMP['color'][i]
            ax.axhline(y=T, alpha=0.3, color=c)

        for ax in axs:
            ax.grid(True, which='both')
            ax.legend().set_visible(False)
            for t in self.TorqueMeasurementPoints[self.TorqueMeasurementPoints['Time'] != 0.0]['Time']:
                ax.axvline(x=t, alpha=0.2, color='red')
            for index, row in self.df_StepResult.iterrows():
                #print(index)
                t = row['StartTime']            
                ax.axvline(x=t, alpha=0.2, color='red')
            
        
        fig.set_size_inches(np.r_[250, 250 / 1.4] / 25.4)
        fig.tight_layout(pad=3, w_pad=1.0, h_pad=1.0)
        
        return fig
    
    def plot_trace_angle(self, fig=None):
        if fig:
            ax = fig.axes[0]
        else:
            fig, ax = plt.subplots(1, 1)
        fig.canvas.set_window_title('{} Trace Angle Plot'.format(self.title()))

        selfrace = self.TracePoints.copy()
        anglemax = self.TracePoints['Angle Median in deg'].max()
        selfrace['Angle0 Median in deg'] = self.TracePoints['Angle Median in deg'] - anglemax

        selfrace.plot(ax=ax, x='Angle0 Median in deg', y='Torque Median in Nm', label=self.title())
        ax.grid(True, which='both')
        ax.set_ylabel('Torque Median in Nm')
        ax.legend().set_visible(False)

        TMP = self._TorqueMeasurementPointsWC()

        for i in self.TorqueMeasurementPoints[self.TorqueMeasurementPoints['Angle'] != 0.0].index:
            a = self.TorqueMeasurementPoints['Angle'][i] - anglemax
            c = TMP['color'][i]
            ax.axvline(x=a, alpha=0.3, color=c)

        for i in self.TorqueMeasurementPoints[self.TorqueMeasurementPoints['Torque'] != 0.0].index:
            T = self.TorqueMeasurementPoints['Torque'][i]
            c = TMP['color'][i]
            ax.axhline(y=T, alpha=0.3, color=c)

        for index, row in self.df_StepResult.iterrows():
            dp = self.df_TracePoints.iloc[self.df_TracePoints.index.get_loc(row['StartTime'], method='nearest')]
            a = dp['Angle Median in deg'] - anglemax
            ax.axvline(x=a, alpha=0.2, color='red')
            ax.axhline(y=dp['Torque Median in Nm'], alpha=0.2, color='red')
    
        fig.set_size_inches(np.r_[250, 250 / 1.4] / 25.4)
        fig.tight_layout(pad=3, w_pad=1.0, h_pad=1.0)
        
        return fig
        

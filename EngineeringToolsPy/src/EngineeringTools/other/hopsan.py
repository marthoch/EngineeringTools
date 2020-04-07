#!/usr/bin/env python3
# pylint: disable-msg=line-too-long,missing-module-docstring,missing-function-docstring,missing-class-docstring,no-else-return,invalid-name,multiple-statements


__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"

try:
    import pandas as pd
    import h5py
except ImportError:
    pass

import logging
logger = logging.getLogger()

def writeHopsanParameterFile(filename, param):
    """write a HCOM script to load parameteres into hopsan

    Args:
        filename (string): name of the file to generate, wil be overwritten if existing.
        param (dict): key: parameter name, value: parameter value

    >>> hopsanParameter = {}
    >>> hopsanParameter['test'] = 123
    >>> hopsanParameter['test2'] = 1244
    >>> writeHopsanParameterFile('testfile.hcom', hopsanParameter)
    """
    with open(filename, 'w') as f:
        f.write('# cd -mwd\n')
        f.write('# exec {}\n'.format(f.name))
        f.write('# all values are in SI base units\n')
        pl = list(param)
        pl.sort()
        #for p, v in param.iteritems():
        for p in pl:
            f.write('adpa {parameterName} {value!r}\n'.format(parameterName=p, value=param[p]))

def read_hopsan_h5(filename):
    def read_group(grp, time=None, data=None):
        logging.debug(grp)
        if data is None:
            data = {}
        groups = []
        datasets = []
        #for name, item in grp.iteritems():  # python 2.8
        for name, item in grp.items():
            if isinstance(item, h5py._hl.group.Group):
                groups.append(item)
            elif isinstance(item, h5py._hl.dataset.Dataset):
                if name == 'Time':
                    time = item
                else:
                    datasets.append(item)
            else:
                logging.warning('Unknown item ignored: {} {}'.format(item.name, type(item)))
        for ds in datasets:
            data[ds.name] = pd.Series(data=ds, index=time, name=ds.name)
        for gr in groups:
            read_group(gr, time=time, data=data)
        return data


    with h5py.File(filename, mode='r') as h5file:
        data = read_group(h5file)
    return pd.DataFrame.from_dict(data)


def read_hopsan_h5_dict(filename):

    def read_group(grp, time=None, data=None):
        logging.debug(grp)
        if data is None:
            data = {}
        groups = []
        datasets = []
        for name, item in grp.items():
            if isinstance(item, h5py._hl.group.Group):
                groups.append(item)
            elif isinstance(item, h5py._hl.dataset.Dataset):
                if name == 'Time':
                    time = item
                else:
                    datasets.append(item)
            else:
                logging.warning('Unknown item ignored: {} {}'.format(item.name, type(item)))
        datag = {}
        for ds in datasets:
            datag[ds.name] = pd.Series(data=ds, index=time, name=ds.name)
        data['ds'] = pd.DataFrame.from_dict(datag)
        for gr in groups:
            datagroup = {}
            data[gr.name.split(r'/')[-1]] = datagroup
            read_group(gr, time=time, data=datagroup)
        return data


    with h5py.File(filename, mode='r') as h5file:
        data = read_group(h5file)
    return data['results']



def read_hopsan_h5_dictflat(filename):

    def read_group(grp, result, time=None):
        logging.debug(grp)
        groups = []
        datasets = []
        localtime = False
        for name, item in grp.items():
            if isinstance(item, h5py._hl.group.Group):
                groups.append(item)
            elif isinstance(item, h5py._hl.dataset.Dataset):
                if name == 'Time':
                    time = item
                    localtime = True
                else:
                    datasets.append(item)
            else:
                logging.warning('Unknown item ignored: {} {}'.format(item.name, type(item)))

        data = {}
        for gr in groups:
            #datagroup = {}
            #data[gr.name.split(r'/')[-1]] = datagroup
            datagroup, grouphaslocaltime = read_group(gr, result=result, time=time)
            if grouphaslocaltime:
                result[gr.name] = pd.DataFrame.from_dict(datagroup)
            else:
                data.update(datagroup)
        for ds in datasets:
            if ds.shape != time.shape:
                print("""Data set does not fit time vector
{ds.name}
{ds.shape}
{time.name}
{ds}                
""".format(ds=ds, time=time))
            else:
                data[ds.name] = pd.Series(data=ds, index=time, name=ds.name)
        return data, localtime

    result = {}
    with h5py.File(filename, mode='r') as h5file:
        data = read_group(h5file, result=result)
    return result

# eif

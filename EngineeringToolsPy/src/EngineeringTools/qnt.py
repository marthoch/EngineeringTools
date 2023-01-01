#!/usr/bin/env python3
# pylint: disable=line-too-long,no-else-return

""" quantize a value

content:
========
    some functions for rounding and quantization

@summary: quantize a value

# old format defaults for test
>>> FORMAT_DEFAULT['totalWidth'] = 8
>>> FORMAT_DEFAULT['decimalPosition'] = 4
>>> FORMAT_DEFAULT['thousands_sep'] = ''

"""

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"


# $Source$
import math
import logging


FORMAT_DEFAULT = {'totalWidth':14, 'decimalPosition':10, 'thousands_sep':' '}

_rtab = {}
_rtab['0.01'] = {'method':'threshold', 'threshold':0.01,
                 'addPrecision': 0,
                 '__doc__':'round up if rest >= 0.01'}
_rtab['0.10'] = {'method':'threshold', 'threshold':0.10,
                 'addPrecision': 0,
                 '__doc__':'round up if rest >= 0.10'}
_rtab['0.25'] = {'method':'threshold', 'threshold':0.25,
                 'addPrecision': 0,
                 '__doc__':'round up if rest >= 0.25'}
_rtab['0.50'] = {'method':'threshold', 'threshold':0.50,
                 'addPrecision': 0,
                 '__doc__':'round up if rest >= 0.50'}
_rtab['0.75'] = {'method':'threshold', 'threshold':0.75,
                 'addPrecision': 0,
                 '__doc__':'round up if rest >= 0.75'}
_rtab['0.90'] = {'method':'threshold', 'threshold':0.90,
                 'addPrecision': 0,
                 '__doc__':'round up if rest >= 0.98'}
_rtab['0.99'] = {'method':'threshold', 'threshold':0.99,
                 'addPrecision': 0,
                 '__doc__':'round up if rest >= 0.99'}
_rtab['1']    = {'method':'quant', 'quant':1.0,
                 'addPrecision': 0,
                 '__doc__':'like round'}
_rtab['2']    = {'method':'quant', 'quant':2.0,
                 'addPrecision': 0,
                 '__doc__':'0, 2, 4, 6, 8, 10'}
_rtab['2.5']  = {'method':'quant', 'quant':2.5,
                 'addPrecision': 1,
                 '__doc__':'0.0, 2.5, 5.0, 7.5, 10'}
_rtab['1/3']  = {'method':'quant', 'quant':1.0/3.0,
                 'addPrecision': 1,
                 '__doc__':'0, 1/3, 2/3, 1'}
_rtab['5']    = {'method':'quant', 'quant':5.0,
                 'addPrecision': 0,
                 '__doc__':'0, 5, 10'}

# Normzahlen nach DIN 323: [Roloff_Maschinenelemente_11_1987 Tab-A2-1]
_rtab['R5']   = {'method':'stdnum',
                 '__doc__':'Normzahlenreihe R5  nach DIN 323: [Roloff_Maschinenelemente_11_1987 Tab-A2-1]',
                 'addPrecision': 2,
                 'tab':[1.00, 1.60, 2.50, 4.00, 6.30]}
_rtab['R10']  = {'method':'stdnum',
                 '__doc__':'Normzahlenreihe R10 nach DIN 323: [Roloff_Maschinenelemente_11_1987 Tab-A2-1]',
                 'addPrecision': 2,
                 'tab':[1.00, 1.25, 1.60, 2.00, 2.50, 3.15, 4.00, 5.00, 6.30, 8.00]}
_rtab['R20']  = {'method':'stdnum',
                 '__doc__':'Normzahlenreihe R20 nach DIN 323: [Roloff_Maschinenelemente_11_1987 Tab-A2-1]',
                 'addPrecision': 2,
                 'tab':[1.00, 1.12, 1.25, 1.40, 1.60, 1.80, 2.00, 2.24, 2.50, 2.80,
                        3.15, 3.55, 4.00, 4.50, 5.00, 5.60, 6.30, 7.10, 8.00, 9.00]}
_rtab['R40']  = {'method':'stdnum',
                 '__doc__':'Normzahlenreihe R40 nach DIN 323: [Roloff_Maschinenelemente_11_1987 Tab-A2-1]',
                 'addPrecision': 2,
                 'tab':[1.00, 1.06, 1.12, 1.18, 1.25, 1.32, 1.40, 1.50, 1.60, 1.70,
                        1.80, 1.90, 2.00, 2.12, 2.24, 2.36, 2.50, 2.65, 2.80, 3.00,
                        3.15, 3.35, 3.55, 3.75, 4.00, 4.25, 4.50, 4.75, 5.00, 5.30,
                        5.60, 6.00, 6.30, 6.70, 7.10, 7.50, 8.00, 8.50, 9.00, 9.50]}



def list_methods():
    """list the available quantization methods"""
    print('methods of quantization:')
    print('-'*72)
    for method in sorted(_rtab.keys()):
        print('%-8s %-12s %s' % (("'%s'" % method),
                                 _rtab[method]['method'],
                                 _rtab[method].get('__doc__', '')))
    print('-'*72)



def quant(val, method='1', precision=0, rettype=None, **formatdef):
    """quantize val with method to precision


    some examples:
    ==============

        >>> print(quant(1234.56789, '1'))
        1235.0
        >>> print(quant(1234.56789, '1', 0, rettype='both'))
        (1235.0, '1235    ')
        >>> print(quant(1234.56789, '1-', 0, rettype='both'))
        (1234.0, '1234    ')
        >>> print(quant(1234.56789, '1--', 0, rettype='both'))
        (1234.0, '1234    ')
        >>> print(quant(1234.56789, '1+', 0, rettype='both'))
        (1235.0, '1235    ')
        >>> print(quant(1234.56789, '1++', 0, rettype='both'))
        (1235.0, '1235    ')

        >>> print(quant(1234.56789, '1', -2, rettype='both'))
        (1200.0, '1200    ')

        >>> print(quant(1234.56789, '2-', 1, rettype='both'))
        (1234.4, '1234.4  ')

        >>> print(quant(1234.56789, '1r', 3, rettype='both'))
        (1230.0, '1230    ')
        >>> print(quant(1234.56789, '1_r', 3, rettype='both'))
        (1230.0, '1230    ')
        >>> print(quant(1234.56789, '1+r', 3, rettype='both'))
        (1240.0, '1240    ')
        >>> print(quant(1234.56789, '1++r', 3, rettype='both'))
        (1240.0, '1240    ')
        >>> print(quant(1234.56789, '1r', 1, rettype='both'))
        (1000.0, '1000    ')
        >>> print(quant(1234.56789, '1r', 2, rettype='both'))
        (1200.0, '1200    ')
        >>> print(quant(1234.56789, '1r', 4, rettype='both'))
        (1235.0, '1235    ')

        >>> print(quant(1234.56789, '0.10', 1, rettype='both'))
        (1234.6000000000001, '1234.6  ')
        >>> print(quant(1234.56789, '0.75', 1, rettype='both'))
        (1234.5, '1234.5  ')

        >>> print(quant(1010.0, '0.10', -2, rettype='both'))
        (1100, '1100    ')
        >>> print(quant(1009.999999999, '0.10', -2, rettype='both'))
        (1000, '1000    ')

        >>> print(quant(1110, '1/3', -2, rettype='both'))
        (1099.9999999999998, '1100    ')

        >>> print(quant(1120, '1/3', -2, rettype='both'))
        (1133.3333333333333, '1133    ')

        >>> print(quant(4251, 'R40', -2, rettype='both'))
        (4250.0, '4250    ')

        >>> print(quant(0.0797885, 'R5', rettype='both'))
        (0.1, '   0.10 ')

        >>> print(quant(0.0, '1', rettype='both'))
        (0.0, '   0    ')
        >>> print(quant(0.0, '1r', rettype='both'))
        (0.0, '   0    ')
        >>> print(quant(0.0, 'R5', rettype='both'))
        (0.0, '   0.00 ')

    @param val: value to quantize
    @type  val: float, int, long

    @param method: method of quantization

      To list all the available methods of quantization use::
        qnt.list_methods()

      there are some postfixes::
        'method-'   round towards 0.0
                     often it is better to use '0.99'
        'method--'  round towards -infinity
        'method+'   round away from 0.0
                     often it is better to use '0.01'
        'method++'  round towards +infinity
        'method..r' precision is relative

      important methods are::
        '1' .... like round
        '2' .... 0, 2, 4, 6, 8, 10
        '2.5' .. 0.0, 2.5, 5.0, 7.5, 10
        '5' .... 0, 5, 10
        'R10' .. Normzahlenreihe R10 nach DIN 323: [Roloff_Maschinenelemente_11_1987 Tab-A2-1]
        'R20' .. Normzahlenreihe R20 nach DIN 323: [Roloff_Maschinenelemente_11_1987 Tab-A2-1]
        'R5' ... Normzahlenreihe R5  nach DIN 323: [Roloff_Maschinenelemente_11_1987 Tab-A2-1]
        '0.01' . round up if rest >= 0.01
        '0.10' . round up if rest >= 0.10
        '0.25' . round up if rest >= 0.25
        '0.90' . round up if rest >= 0.90
        '0.99' . round up if rest >= 0.99
    @type method: str

    @param precision: precision to round,
    can be negative,
    some methods ignore this parameter
    @type precision: int

    @return: quant returns a float

    Args:
        rettype:


    """

    if 'type' in formatdef:
        logging.critical('parameter type provided, use rettype')

    format_ = dict(FORMAT_DEFAULT)
    format_.update(formatdef)

    relative = False
    if method[-2:] == '_r':
        relative = True
        method = method[:-2]
    elif method[-1:] == 'r':  # pylint: disable=E1136
        relative = True
        method = method[:-1]

    if precision is None:
        if relative:
            precision = 3
        else:
            precision = 0
    if relative and precision < 1:
        precision = 3

    if method[-2:] == '++':
        method = method[:-2]
        rnd = math.ceil
    elif method[-1] == '+':  # pylint: disable=E1136
        method = method[:-1]
        rnd = lambda n: math.floor(n) if n < 0.0 else math.ceil(n)
    elif method[-2:] == '--':  # pylint: disable=E1136
        method = method[:-2]
        rnd = math.floor
    elif method[-1] == '-':  # pylint: disable=E1136
        method = method[:-1]
        rnd = lambda n: math.ceil(n) if n < 0.0 else math.floor(n)
    else:
        rnd = round

    rtab = _rtab.get(method, {'method':None})
    if relative:
        if abs(val) < 1.0e-256:
            precision = int(0)
        else:
            precision = int(precision - math.floor(math.log10(abs(val))) - 1)
    else:
        precision = int(precision)

    if rtab['method'] == 'quant':
        k = float(rtab['quant'])*10**(-precision)
        res = rnd(val/k)*k
    elif rtab['method'] == 'threshold':
        k = 10**(-precision)
        rnd = lambda n: math.ceil(n - (1-rtab['threshold'])) if n < 0.0 else math.floor(n + (1-rtab['threshold']))
        res = rnd(val/k)*k
    elif rtab['method'] == 'stdnum':
        if abs(val) < 1e-99:
            res = 0.0
        else:
            N = len(rtab['tab'])
            k = 10.0**(1.0/N)
            valabs = abs(val)
            sign = -1.0 if val < 0.0 else 1.0
            e = math.floor(math.log10(valabs))
            i = math.log(valabs / (10.0**e)) / math.log(k)
            i = abs(int(rnd(sign*i)))
            if i == N:
                i = 0
                e += 1
            res = sign*(10.0**e) * rtab['tab'][i]
    else:
        raise Exception('method not known')

    precision_s = precision + rtab['addPrecision']
    precision_s = precision_s if precision_s > 0 else 0
    width = format_.get('decimalPosition', 0) + precision_s + 1
    if precision_s == 0:
        width  -= 1
    width_ext = format_.get('totalWidth', 0) - width
    width_ext = width_ext if width_ext >= 0 else 0
    tsep = format_.get('thousands_sep', '')
    tsepx = ',' if tsep else ''
    strrep = f"{res:{width}{tsepx}.{precision_s}f}" + width_ext*' '
    if tsep:
        strrep = strrep.replace(',', tsep)

    if not rettype or rettype == 'float':
        return res
    elif rettype == 'string':
        return strrep
    elif rettype == 'both':
        return res, strrep
    else:
        raise Exception('type not known')

# some alias

def r5(val): # IGNORE:C0103
    """Normzahlenreihe R5
    nach DIN 323: [Roloff_Maschinenelemente_11_1987 Tab-A2-1]"""
    return quant(val, method='R5', precision=None)


def r10(val):
    """Normzahlenreihe R10
    nach DIN 323: [Roloff_Maschinenelemente_11_1987 Tab-A2-1]"""
    return quant(val, method='R10', precision=None)


def r20(val):
    """Normzahlenreihe R20
    nach DIN 323: [Roloff_Maschinenelemente_11_1987 Tab-A2-1]"""
    return quant(val, method='R20', precision=None)

def r40(val):
    """Normzahlenreihe R40
    nach DIN 323: [Roloff_Maschinenelemente_11_1987 Tab-A2-1]"""
    return quant(val, method='R40', precision=None)


def _test():
    """run doctest"""
    import doctest # pylint: disable=import-outside-toplevel
    doctest.testmod()


def _my_test():
    """simple test"""

    def test_round(N=15, inc=1.0, method='1', precision=None):
        for i in range(0, N, 1) + range(0, -N, -1):
            n = i*inc
            r = quant(n, method, precision)
            print('%10g %10g %10g' % (n, r, (r+1e-99)/(n+1e-99)))
            n += inc


    test_round(15, 1.0, '0.99', -1)
    list_methods()

    print(quant(0.0797885, 'R5'))



if __name__ == '__main__':
    list_methods()

    #_my_test()

    _test()
# eof

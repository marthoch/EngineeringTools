#!/usr/bin/env python3
# pylint: disable-msg=line-too-long,missing-module-docstring,missing-function-docstring,missing-class-docstring,no-else-return,invalid-name,multiple-statements

"""interpolation function generator
"""

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"

# $Source$


class InterpolateException(Exception):
    """InterpolateException"""


def _find_interval(x, x_vec):
    """find the interval / index of x in x_vec"""
    for i in range(len(x_vec) - 1):
        if (x >= x_vec[i]) and (x < x_vec[i+1]):
            return i
    raise InterpolateException('x is out of range: x=%s in [%s : %s[' \
                                % (x, x_vec[0], x_vec[-1]))


def _cholesky_s_t_p(d, a, b):
    """loesen eines Gleichungssystem

    mit symmetrischer, tridiagonaler, positiv definiter Matrix
    see: Bartsch19: Taschenbuch der Mathematischen Formeln, page 183

    >>> d = [1.0, 2.0, 3.0, 4.0]
    >>> a = [1.5, 2.5, 3.5]
    >>> b = [10.0, 20.0, 30.0, 40.0]
    >>> print(_cholesky_s_t_p(d, a, b))
    [12.932330827067668, -1.954887218045112, 1.8045112781954888, 8.421052631578947]
    """
    #check
    N = len(d)
    if N != len(b):
        raise InterpolateException('len(d) != len(b)')
    if N != len(a)+1:
        raise InterpolateException('len(d) != len(a)+1')


    # 1
    delta = [None]*N
    rho = [None]*(N-1)
    delta[0] = d[0]
    rho[0] = a[0] / delta[0]
    for i in range(1, N-1):
        delta[i] = d[i] - a[i-1] * rho[i-1]
        rho[i] = a[i] / delta[i]
    delta[N-1] = d[N-1] - a[N-2] * rho[N-2]

    # 2
    z = [None]*N
    z[0] = b[0]
    for i in range(1, N):
        z[i] = b[i] - rho[i-1]*z[i-1]
    c = [z[i] / delta[i] for i in range(N)]

    # 3
    x = [None]*N
    x[N-1] = c[N-1]
    for i in range(N-2, -1, -1):
        x[i] = c[i] - rho[i]*x[i+1]

    return x


def _get_interpolate_spline(x_vec, y_vec, **vargsd):
    if len(x_vec) == 2:
        if 'dydx_a' not in vargsd and 'dydx_b' not in vargsd:
            a = [y_vec[0]]
            b = [(y_vec[1]-y_vec[0])/(x_vec[1]-x_vec[0])]
            c = [0.0]
            d = [0.0]
        elif 'dydx_a' not in vargsd and 'dydx_b' in vargsd:
            h = (x_vec[1]-x_vec[0])
            a = [y_vec[0]]
            c = [0.0]
            d = [(vargsd['dydx_b']*h + y_vec[0]-y_vec[1]) / (2*h**3)]
            b = [vargsd['dydx_b'] - 3*d[0]*h**2]
        elif 'dydx_a' in vargsd and 'dydx_b' not in vargsd:
            h = (x_vec[1]-x_vec[0])
            a = [y_vec[0]]
            b = [vargsd['dydx_a']]
            d = [(y_vec[0] - y_vec[1] + vargsd['dydx_a']*h) / (2*h**3)]
            c = [-3*d[0]*h]
        elif 'dydx_a' in vargsd and 'dydx_b' in vargsd:
            h = (x_vec[1]-x_vec[0])
            a = [y_vec[0]]
            b = [vargsd['dydx_a']]
            d = [(vargsd['dydx_b'] - vargsd['dydx_a'] - 2/h*(y_vec[1]-y_vec[0])) / (h**2)]
            c = [(vargsd['dydx_b'] - b[0] - 3*d[0]*h**2) / (2*h)]
    elif len(x_vec) == 3:
        a = list(y_vec)
        b = [None]*2
        c = [None]*3
        d = [None]*2
        h = [x_vec[i+1] -x_vec[i] for i in range(2)]

        c[0] = 0.0
        c[1] = (1/h[1]*(a[2]-a[1]) -1/h[0]*(a[1]-a[0])) / (2/3*(h[0]+h[1]))
        c[2] = 0.0

        for i in range(2):
            b[i] = 1/h[i]*(a[i+1] - a[i]) - h[i]/3*(c[i+1] + 2*c[i])
            d[i] = 1/(3*h[i])*(c[i+1] - c[i])

        a = a[:2]
        c = c[:2]

    else:
        # spline interpolation;
        # see: Bartsch19: Taschenbuch der Mathematischen Formeln, page 317
        a = list(y_vec)
        N = len(a)
        n = N - 1
        h = [x_vec[i+1] -x_vec[i] for i in range(n)]

        eq_d = [None]*(n+1)
        eq_a = [None]*n
        eq_b = [None]*(n+1)

        # i=1
        if 'dydx_a' in vargsd:
            eq_d[1] = 3/2*h[0] + 2*h[1] # Bartsch19 Druckfehler 2/3 => 3/2
            eq_a[1] = h[1]
            eq_b[1] = 3/h[1]*(a[2]-a[1]) - 9/(2*h[0])*(a[1]-a[0]) + 3/2*vargsd['dydx_a']
        else:
            eq_d[1] = 2*(h[0] + h[1])
            eq_a[1] = h[1]
            eq_b[1] = 3/h[1]*(a[2]-a[1]) - 3/h[0]*(a[1]-a[0])

        # i = 2..n-2
        for i in range(2, n-1):
            eq_d[i] = 2*(h[i-1] + h[i])
            eq_a[i] = h[i]
            eq_b[i] = 3/h[i]*(a[i+1]-a[i]) - 3/h[i-1]*(a[i]-a[i-1])

        # i = n-1
        if 'dydx_b' in vargsd:
            eq_d[n-1] = 2*h[n-2] + 3/2*h[n-1]
            eq_a[n-1] = 0.0
            eq_b[n-1] = 9/(2*h[n-1])*(a[n]-a[n-1]) - 3/2*vargsd['dydx_b'] \
                        - 3/h[n-2]*(a[n-1]-a[n-2])
        else:
            i = n-1
            eq_d[i] = 2*(h[i-1] + h[i])
            eq_a[i] = h[i]
            eq_b[i] = 3/h[i]*(a[i+1]-a[i]) - 3/h[i-1]*(a[i]-a[i-1])


        c = _cholesky_s_t_p(eq_d[1:-1], eq_a[1:-1], eq_b[1:-1])
        c.insert(0, None)
        c.append(None)
        if 'dydx_a' in vargsd:
            c[0] = 1/(2*h[0]) * (3/h[0]*(a[1]-a[0]) \
                                 - 3*vargsd['dydx_a'] - c[1]*h[0])
        else:
            c[0] = 0.0
        if 'dydx_b' in vargsd:
            c[n] = -1/(2*h[n-1]) * (3/h[n-1]*(a[n]-a[n-1]) \
                                    - 3*vargsd['dydx_b'] + c[n-1]*h[n-1])
        else:
            c[n] = 0.0

        b = [None]*(n+1)
        d = [None]*(n+1)
        for i in range(n):
            b[i] = 1/h[i]*(a[i+1] - a[i]) - h[i]/3*(c[i+1] + 2*c[i])
            d[i] = 1/(3*h[i])*(c[i+1] - c[i])

        a = a[:n]
        b = b[:n]
        c = c[:n]
        d = d[:n]

    def interpolate(x): #IGNORE:C0103
        """spline interpolation
        see: Bartsch19: Taschenbuch der Mathematischen Formeln, page 317
        """
        if x == x_vec[-1]:  # float: == is correct
            return y_vec[-1]
        i = _find_interval(x, x_vec)
        d_x = x - x_vec[i]
        y = a[i]  + b[i]*d_x + c[i]*d_x**2 + d[i]*d_x**3
        return y
    return interpolate


def get_interpolate(x_vec, y_vec, method=None, **vargsd):
    """
    >>> x_vec = (0.0,  1.0,  2.0)
    >>> y_vec = (0.0, 10.0, 20.0)
    >>> f = get_interpolate(x_vec, y_vec)
    >>> print(f(0.0))
    0.0
    >>> print(f(2.0))
    20.0
    >>> print(f(0.99))
    9.9

    >>> print(f(-3))
    Traceback (most recent call last):
    ..
    EngineeringTools.tools.interpolate.InterpolateException: x is out of range: x=-3 in [0.0 : 2.0[

    >>> print(f(3))
    Traceback (most recent call last):
    ...
    EngineeringTools.tools.interpolate.InterpolateException: x is out of range: x=3 in [0.0 : 2.0[

    >>> f = get_interpolate((2, 1), (1, 2))
    Traceback (most recent call last):
    ...
    EngineeringTools.tools.interpolate.InterpolateException: x_vec is not monotone

    >>> f = get_interpolate((0, 1, 2, 3, 4), (0, 1, 2, 3, 4), method='spline')
    >>> print(f(0.0))
    0.0
    >>> print(f(1.5))
    1.5
    """
    # make some checks
    if len(x_vec) != len(y_vec):
        raise InterpolateException('length of x_vec and y_vec do not match')
    if len(x_vec) < 2:
        raise InterpolateException('min length of x_vec is 2')

    for i in range(len(x_vec)-1):
        if x_vec[i+1] < x_vec[i]:
            raise InterpolateException('x_vec is not monotone')

    if method in (None, 'linear'):
        def interpolate(x): #IGNORE:C0103
            """linear interpolation"""
            if x == x_vec[-1]:  # float: == is correct
                return y_vec[-1]
            i = _find_interval(x, x_vec)
            y = y_vec[i] + (x - x_vec[i]) * ((y_vec[i+1] - y_vec[i])
                                             / (x_vec[i+1] - x_vec[i]))
            return y
    elif method == 'before':
        def interpolate(x): #IGNORE:C0103
            """interpolation before"""
            if x == x_vec[-1]:  # float: == is correct
                return y_vec[-1]
            i = _find_interval(x, x_vec)
            y = x_vec[i]
            return y
    elif method == 'after':
        def _find_interval_(x, x_vec):
            """find the interval / index of x in x_vec
            special version for 'after'
            """
            for i in range(len(x_vec) - 1):
                if (x > x_vec[i]) and (x <= x_vec[i+1]):
                    return i
            raise InterpolateException('x is out of range: x=%s in ]%s : %s]' \
                                        % (x, x_vec[0], x_vec[-1]))

        def interpolate(x): #IGNORE:C0103
            """interpolation after"""
            if x == x_vec[0]:  # float: == is correct
                return y_vec[0]
            i = _find_interval_(x, x_vec)
            y = x_vec[i+1]
            return y
    elif method == 'spline':
        interpolate = _get_interpolate_spline(x_vec, y_vec, **vargsd)
    else:
        raise InterpolateException('method not found: %s' % method)

    return interpolate

# TESTS =========================================================================


def do_plot_test(x_vec, y_vec, method=None, n=1001, **vargsd):
    """plot of interpolation to do an optical verify """

    interpolf = get_interpolate(x_vec, y_vec, method=method, **vargsd)

    xf_tmp = list(x_vec)
    xtmp = xf_tmp.pop(0)
    xf_vec = []
    yf_vec = []
    xmin = x_vec[0]
    k = (x_vec[-1]-xmin)/(n-1)
    for i in range(n):
        xf = xmin + i*k
        if xf_tmp and (xf >= xtmp):
            if xf > xtmp:
                xf_vec.append(xtmp)
                yf_vec.append(interpolf(xtmp))
            xtmp = xf_tmp.pop(0)
        xf_vec.append(xf)
        yf_vec.append(interpolf(xf))
    yf_dx_vec = [(yf_vec[i+1] - yf_vec[i])/(xf_vec[i+1] - xf_vec[i])
                 for i in range(n-1)]
    yf_dxx_vec = [(yf_dx_vec[i+1] - yf_dx_vec[i])/(xf_vec[i+1] - xf_vec[i])
                  for i in range(n-2)]

    import pylab
    pylab.figure(1)
    pylab.subplot(311)
    pylab.plot(x_vec, y_vec, 'ro')
    pylab.plot(xf_vec, yf_vec, 'b')
    pylab.subplot(312)
    pylab.plot(xf_vec[:-1], yf_dx_vec)
    pylab.subplot(313)
    pylab.plot(xf_vec[:-2], yf_dxx_vec)
    pylab.show()


def _test():
    """run doctest"""
    import doctest # pylint: disable=import-outside-toplevel
    from EngineeringTools import quantities as ETQ             # pylint: disable=reimported,import-outside-toplevel
    ETQ.Quantity.set_displayUnitSystem('mechanicalEngineering')
    module_name = 'EngineeringTools.tools.interpolate'         # pylint: disable=invalid-name
    module = __import__(module_name, fromlist=['*'], level=0)  # pylint: disable=invalid-name
    print(doctest.testmod(module, optionflags=doctest.ELLIPSIS))


def test_plot():
    #x_vec_ = (0, 1, 2, 3, 4, 8, 10)
    x_vec_ = (0, 1, 2)
    #y_vec_ = (0, 1, 0, -1, 0, 5, 3)
    #y_vec_ = [x for x in x_vec_]
    #y_vec_ = [x**2 for x in x_vec_]
    #y_vec_ = [x**3 for x in x_vec_]
    #y_vec_ = [x**3 for x in x_vec_]
    y_vec_ = [0, 1, 0]

    #f = get_interpolate(x_vec_, y_vec_)
    #f = get_interpolate(x_vec_, y_vec_, method='linear')
    #f = get_interpolate(x_vec_, y_vec_, method='before')
    #f = get_interpolate(x_vec_, y_vec_, method='after')
    #f = get_interpolate(x_vec_, y_vec_, method='spline')
    #f = get_interpolate(x_vec_, y_vec_, method='spline', dydx_a=0.0)
    #print f(1.0)

    #do_plot_test(x_vec_, y_vec_, method='linear')
    #do_plot_test(x_vec_, y_vec_, method='before')
    #do_plot_test(x_vec_, y_vec_, method='after')

    #do_plot_test([0, 1], [0, 1], method='spline')
    #do_plot_test([0, 1], [0, 1], method='spline', dydx_a=0.0)
    #do_plot_test([0, 1], [0, 1], method='spline', dydx_b=0.0)
    #do_plot_test([0, 1], [0, 1], method='spline', dydx_a=0.0, dydx_b=0.0)
    #do_plot_test(x_vec_, y_vec_, method='spline')
    #do_plot_test(x_vec_, y_vec_, method='spline', dydx_a=0.0)
    #do_plot_test(x_vec_, y_vec_, method='spline', dydx_b=0.0)
    #do_plot_test(x_vec_, y_vec_, method='spline', dydx_a=0.0, dydx_b=0.0)
    #do_plot_test(x_vec_, y_vec_, method='spline', dydx_a=1.0, dydx_b=-1.0)

if __name__ == '__main__':
    _test()
    #test_plot()

#eof


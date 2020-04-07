#!/usr/bin/env python3
# pylint: disable-msg=line-too-long,missing-module-docstring,missing-function-docstring,missing-class-docstring,no-else-return,invalid-name,multiple-statements

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"

import numpy as np

def cross(series, cross=0, direction='cross'):
    """
    Given a Series returns all the index values where the data values equal 
    the 'cross' value. 

    Direction can be 'rising' (for rising edge), 'falling' (for only falling 
    edge), or 'cross' for both edges

    returns: the index values when crossing (interpolated) and the index befor and after the crossing

    copy from: http://stackoverflow.com/questions/10475488/calculating-crossing-intercept-points-of-a-series-or-dataframe
    with some extensions
    """
    # Find if values are above or bellow yvalue crossing:
    above = series.values > cross
    below = np.logical_not(above)
    left_shifted_above = above[1:]
    left_shifted_below = below[1:]

    # Find indexes on left side of crossing point
    if direction == 'rising':
        idxs = (left_shifted_above & below[0:-1]).nonzero()[0]
    elif direction == 'falling':
        idxs = (left_shifted_below & above[0:-1]).nonzero()[0]
    else:
        rising = left_shifted_above & below[0:-1]
        falling = left_shifted_below & above[0:-1]
        idxs = (rising | falling).nonzero()[0]

    # Calculate x crossings with interpolation using formula for a line:
    x1 = series.index.values[idxs]
    x2 = series.index.values[idxs+1]
    y1 = series.values[idxs]
    y2 = series.values[idxs+1]
    x_crossings = (cross-y1)*(x2-x1)/(y2-y1) + x1

    return x_crossings, series.index[idxs], series.index[idxs+1]

# eof
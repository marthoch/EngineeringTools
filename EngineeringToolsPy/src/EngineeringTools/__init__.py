#!/usr/bin/env python3
"""EngineeringTools

# Quantities

The main kind of objects (super class) in EngineeringTools are Quantities.
A Quantity represents a physical quantity like length/distance or energy.

One goal within EngineeringTools is to avoid mistakes, or at least detect as
 many as possible. One source of mistakes is unit conversions. Quantities can be
 used the convert values between various units.
`ETQ.Distance(1, 'm').get_value('mm')   … 1000`

One other source of mistake is error in equations. One known way to detect this
kind of mistake is to check the plausibility of a calculation based on the units
of the operands. This check cannot guaranty that the calculation is correct, but
many incorrect cases can be detected.
For calculations, quantities are not sufficient as not every intermediate result
does correspond with defined quantities. Therefore, UVals are used for
intermediate results. UVal’s units are represented in base units (kg, m, s, …)
which are used to check the calculation. Quantities are automatically converted
to UVals where necessary. By converting them back to Quantities it is checked
whether the result’s unit fits with the expects Quantity.
`Area( Distance(1,’m’)* Distance(1,’m’))`


## Mathematical functions: sin, tan, ...
The functions for the standard module math or for numpy do not recognize
Quantities or UVals. Therefore, the function from EngineeringTools.tools must be
used which are usually imported as `ETtools`.


>>> # add EngineeringTools to python path if required
>>> import sys
>>> sys.path.insert(0, r'C:/data/GitHub/EngineeringTools/EngineeringToolsPy/src')
>>>
>>> import EngineeringTools.quantities as ETQ    # quantities
>>> from EngineeringTools.other import Obj
>>> from EngineeringTools.tools import tools as ETtools  # sin, cos, tan, ....
>>> ETQ.Quantity.set_displayUnitSystem('mechanicalEngineering')  # specifying default unit system

"""

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"

# $Source$
from . import quantities as Q
from .quantities import *
from . import tools
from .tools.functions import *
from .container import Obj, REQ

from . import fluidpower_eng
from . import mechanical_eng

# eof

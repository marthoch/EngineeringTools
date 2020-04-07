#!/usr/bin/env python3
# pylint: disable-msg=line-too-long,missing-module-docstring,missing-function-docstring,missing-class-docstring,no-else-return,invalid-name

"""
# doctest
# reset new format defaults for test
>>> from EngineeringTools.quantities import qnt
>>> qnt.FORMAT_DEFAULT['totalWidth'] = 14
>>> qnt.FORMAT_DEFAULT['decimalPosition'] = 10
>>> qnt.FORMAT_DEFAULT['thousands_sep'] = ' '
"""

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"


# run doctest, workaround relative import
if __name__ == '__main__':
    import sys
    import doctest # pylint: disable=import-outside-toplevel
    module_name = 'EngineeringTools.mechanical_eng.buckling'        # pylint: disable=invalid-name
    module = __import__(module_name, fromlist=['*'], level=0)  # pylint: disable=invalid-name
    module._setup_doctest()                                    # pylint: disable=protected-access
    print(doctest.testmod(module, optionflags=doctest.ELLIPSIS))
    sys.exit()

import logging
import numpy as np

from .. import quantities as ETQ
from ..tools import geo_circle as ETTGC
from EngineeringTools.tools import functions as ETTT
from . import material as M
from . import beamsection as ETMbeamsection

__all__ = ['buckling_euler', 'Buckling']


class Buckling:
    """
    Hamrock 2005: Fundamentals of Machine Elements: page 373++
    steger1988_TechnischeMechanik2: page 156++

    >>> buckling = Buckling()
    >>> buckling.material = M.Steel_S355JR()
    >>> buckling.beamSection = ETMbeamsection.BeamSection_Pipe(D=ETQ.Distance(20., 'mm'))
    >>> buckling.endcondition = 'one end fixed, one pinned'
    >>> buckling.length = ETQ.Distance(1., 'm')
    >>> print(buckling)
    Buckling
    material:               EngineeringTools.mechanical_eng.material.Steel_S355JR
    name:           Steel: S355JR
    identifiers:    ['S355JR', '1.0045', 'St52-3', 'Sweden SS 2132-01']
    density:             7 800     kg/m3 (Density)
    youngs modulus:    210 000     N/mm^2 (Stress)  
    slendernessRatio limit for Euler:         76.4    (Scalar)
    beam section:           BeamSection_Pipe(D=        20.000 mm (Distance), d=         0.000 mm (Distance))
    end condition:          one end fixed, one pinned
    effective length factor:          0.699  (Scalar)
    beam length:                 1 000.000 mm (Distance)
    effective length:              699.000 mm (Distance)
    slenderness ratio:             140      (Scalar)
    method:                 euler
    buckling force:                 33.3   kN (Force)
    safetyFactor:                    6.00   (Scalar)
    forcePermitted:                  5.55  kN (Force)
"""

    endconditioncases = {'both ends pinned':1.0,
                'both ends fixed':0.5,
                'one end fixed, one pinned':0.699,
                'one end fixed, one free':2.0}

    def __init__(self):
        self._safetyFactor = ETQ.Scalar(6.)
        self._material = None
        self._beamsection = None
        self._endcondition = None
        self._effectiveLengthFactor = None
        self._length = None

    def __str__(self):
        return """Buckling
material:               {self.material}\
slendernessRatio limit for Euler: {self.slendernessRatio_limitEuler}
beam section:           {self.beamSection}
end condition:          {self.endcondition}
effective length factor: {self.effectiveLengthFactor}
beam length:            {self.length}
effective length:       {self.lengthEffective}
slenderness ratio:      {self.slendernessRatio}
method:                 {self.methodname}
buckling force:         {self.bucklingForce}
safetyFactor:           {self.safetyFactor}
forcePermitted:         {self.forcePermitted}\
""".format(self=self)


    @property
    def safetyFactor(self):
        return self._safetyFactor

    @safetyFactor.setter
    def safetyFactor(self, safetyFactor):
        if safetyFactor < 3.0:
            logging.warning('The safety factor for usual application shall be between 3.0 and 7.0')
        else:
            self._safetyFactor = ETQ.Scalar(safetyFactor)

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, material):
        if isinstance(material, M.Material):
            self._material = material
        else:
            self._material = None
            raise Exception('"material" is not an instance of EngineeringTools.mechanics.material but {}'.format(type(material)))

    @property
    def slendernessRatio_limitEuler(self):
        return ETQ.Scalar(np.pi * ETTT.sqrt(self.material.youngs_modulus / self.material.Rp()))


    @property
    def beamSection(self):
        return self._beamsection

    @beamSection.setter
    def beamSection(self, beamsection):
        self._beamsection = beamsection

    @property
    def momentOfArea2nd_effective(self):
        return min([self.beamSection.Ix, self.beamSection.Iy])

    @property
    def endcondition(self):
        """
        >>> buckling = Buckling()
        >>> buckling.endcondition = "1"
        Traceback (most recent call last):
        ...
        Exception: End condition "<class 'str'>" is not known. Available are: both ends pinned, both ends fixed, one end fixed, one pinned, one end fixed, one free
        >>> buckling.endcondition = 'both ends pinned'
        >>> print(buckling.endcondition)
        both ends pinned
        >>> print(buckling.effectiveLengthFactor)
                 1.00   (Scalar)
        """
        return self._endcondition

    @endcondition.setter
    def endcondition(self, endcondition):
        if endcondition in self.endconditioncases:
            self._endcondition = endcondition
            self.effectiveLengthFactor = self.endconditioncases[endcondition]
        else:
            self._endcondition = None
            self._effectiveLengthFactor = None
            raise Exception('End condition "{}" is not known. Available are: {}'.format(type(endcondition), ', '.join(self.endconditioncases.keys())))

    @property
    def effectiveLengthFactor(self):
        """
        >>> buckling = Buckling()
        >>> print(buckling.effectiveLengthFactor)
        None

        >>> buckling.effectiveLengthFactor = "a"
        Traceback (most recent call last):
        ...
        AssertionError: value must be a float

        >>> buckling.effectiveLengthFactor = 1.0
        >>> print(buckling.effectiveLengthFactor)
                 1.00   (Scalar)

        """
        return self._effectiveLengthFactor

    @effectiveLengthFactor.setter
    def effectiveLengthFactor(self, effectiveLengthFactor):
        self._effectiveLengthFactor = ETQ.Scalar(effectiveLengthFactor)


    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, length):
        self._length = ETQ.Distance(length)

    @property
    def lengthEffective(self):
        return ETQ.Distance(self.length * self.effectiveLengthFactor)


    @property
    def slendernessRatio(self):
        I = self.momentOfArea2nd_effective
        A = self.beamSection.A
        rg = ETQ.Distance(ETTT.sqrt(I / A ))
        return ETQ.Scalar(self.lengthEffective / rg )


    @property
    def methodname(self):
        if self.slendernessRatio >= self.slendernessRatio_limitEuler:
            return 'euler'
        else:
            raise NotImplementedError('non-elastic case is not implemented')


    @property
    def bucklingForce(self):
        if self.slendernessRatio >= self.slendernessRatio_limitEuler:
            # euler case
            return ETQ.Force((np.pi**2 * self.material.youngs_modulus * self.momentOfArea2nd_effective) / (self.lengthEffective**2))
        else:
            raise NotImplementedError('non-elastic case is not implemented')


    @property
    def forcePermitted(self):
        return ETQ.Force(self.bucklingForce / self.safetyFactor)


    def sizeRoundBarForForce(self, force):
        """size a round bar for a certian force

        >>> buckling = Buckling()
        >>> buckling.material = M.Steel_S355JR()
        >>> buckling.endcondition = 'one end fixed, one pinned'
        >>> buckling.length = ETQ.Distance(2., 'm')
        >>> print(buckling.sizeRoundBarForForce(ETQ.Force(25., 'kN')))
        BeamSection_Pipe(D=        41.201 mm (Distance), d=         0.000 mm (Distance))
        >>> print(buckling)
        Buckling
        material:               EngineeringTools.mechanical_eng.material.Steel_S355JR
        name:           Steel: S355JR
        identifiers:    ['S355JR', '1.0045', 'St52-3', 'Sweden SS 2132-01']
        density:             7 800     kg/m3 (Density)
        youngs modulus:    210 000     N/mm^2 (Stress)  
        slendernessRatio limit for Euler:         76.4    (Scalar)
        beam section:           BeamSection_Pipe(D=        41.201 mm (Distance), d=         0.000 mm (Distance))
        end condition:          one end fixed, one pinned
        effective length factor:          0.699  (Scalar)
        beam length:                 2 000.000 mm (Distance)
        effective length:            1 398.000 mm (Distance)
        slenderness ratio:             136      (Scalar)
        method:                 euler
        buckling force:                150     kN (Force)
        safetyFactor:                    6.00   (Scalar)
        forcePermitted:                 25.0   kN (Force)
        """
        force = ETQ.Force(force)
        ILowerLimit = ETQ.MomentOfAreaSecond((self.safetyFactor * force * self.lengthEffective**2) / (self.material.youngs_modulus * np.pi**2))
        circle = ETTGC.Circle(momentOfAreaSecond = ILowerLimit)
        self.beamSection = ETMbeamsection.BeamSection_Pipe(D=circle.diameter)
        return self.beamSection


def buckling_euler(length, supportcase, momentOfArea2nd, youngs_modulus=None):
    """
    https://en.wikipedia.org/wiki/Buckling
    """
    youngs_modulus = ETQ.Stress(210e3, 'N/mm^2')

    endconditioncases = {'both ends pinned':1.0,
                'both ends fixed':0.5,
                'one end fixed, one pinned':0.699,
                'one end fixed, one free':2.0}


    if isinstance(supportcase, str):
        K = endconditioncases[supportcase]
    elif isinstance(supportcase, float):
        K = supportcase
    else:
        K = supportcase

    #if isinstance(momentOfArea2nd, Q.MomentOfAreaSecond):
    #    I = momentOfArea2nd.uval()


    F = np.pi**2 * youngs_modulus * momentOfArea2nd / (K*length)**2
    F = ETQ.Force(F)

    return F


def _setup_doctest():
    ETQ.Quantity.set_displayUnitSystem('mechanicalEngineering')

# eof


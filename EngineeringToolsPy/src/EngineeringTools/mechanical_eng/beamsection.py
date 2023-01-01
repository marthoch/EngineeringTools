#!/usr/bin/env python3
# pylint: disable-msg=line-too-long,missing-module-docstring,missing-function-docstring,missing-class-docstring,no-else-return,invalid-name,multiple-statements

"""


# doctest
# old format defaults for test
>>> from EngineeringTools.quantities import qnt
>>> qnt.FORMAT_DEFAULT['totalWidth'] = 8
>>> qnt.FORMAT_DEFAULT['decimalPosition'] = 4
>>> qnt.FORMAT_DEFAULT['thousands_sep'] = ''
"""

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"


# $Source$

# run doctest, workaround relative import
if __name__ == '__main__':
    import sys
    import doctest # pylint: disable=import-outside-toplevel
    module_name = 'EngineeringTools.mechanical_eng.beamsection'     # pylint: disable=invalid-name
    module = __import__(module_name, fromlist=['*'], level=0)  # pylint: disable=invalid-name
    module._setup_doctest()                                    # pylint: disable=protected-access
    print(doctest.testmod(module, optionflags=doctest.ELLIPSIS))
    sys.exit()

from .. import quantities as ETQ
from EngineeringTools.tools import functions

class BeamSection:  #IGNORE:R0903
    r"""Beam Section Properties

    Sources:
    ========
        - Formulas for Stress, Strain and structural matrices: Walter D. Pelkey 1994
        - Roark's Formulas for Stress & Strain 6th Edition 1989
        - U{http://www.corusconstruction.com/en/design_and_innovation/structural_design/the_blue_book/section_properties/british_standard_sections/ubs/}


    Tension and compression:
    ========================

      A: area
      -------
        - ETQ.Area m^2
        - A=\int{dA}_A
        - Sz=Fz/A


    Bending:
    ========
      Ix: moment of inertia of an area about x axis
      ---------------------------------------------
        - Stiffness
        - MomentOfAreaSecond m^4
        - Ix = int{y^2*dA}_A
        - Pilkey1994: page20 eq2.4

      Iy: moment of inertia of an area about y axis
      ---------------------------------------------
        - Stiffness
        - MomentOfAreaSecond  m^4
        - Iy = int{x^2*dA}_A
        - Pilkey1994: page20 eq2.4

      Zex (Wx):
      ---------
        - Resistance
        - SectionModulus m^3
        - Zex = Ix/cy
        - Sz  = Mbx/Zex

      Zey (Wy):
      ---------
        - Resistance::
        - SectionModulus m^3
        - Zey = Iy/cx
        - Sz  = Mby/Zey


    Trosion:
    ========
      Jz (Ip): polar moment of inertia of an area
      -------------------------------------------
        - Stiffness
        - MomentOfAreaSecond  m^4
        - Jz  = \int{r^2*dA}_A = Ix+Iy
        - phi = Mz*L/(G*Jz)
        - Pilkey1994: page22 eq2.10

      Zez (Wp):
      ---------
        - Resistance
        - SectionModulus m^3
        - Wp  = Jz/r
        - tau = Mz/Wp



    Transversal shear Stresses:
    ===========================

      Qx:
      ---
        - MomentOfInertiaOfAreaFirst
        - Resistance
        - Qx=\int{y*dA}_A0

      Qy:
      ---
        - MomentOfInertiaOfAreaFirst
        - Resistance
        - Qy=\int{y*dA}_A0
"""

    def _repr_html_(self):
        return str(self)
    
    def __repr__(self):
        return str(self)



class BeamSection_Rectangle(BeamSection):
    """Beam Cross-Section of a rectangle

    see: L{BeamSection}

        >>> ETQ.Quantity.set_displayUnitSystem('mechanicalEngineering')
        >>> ETQ.Quantity.set_str_quantization(None)
        >>> s = BeamSection_Rectangle(ETQ.Distance(200.0, 'mm'), ETQ.Distance(300.0,'mm'), thickness=ETQ.Distance(12.5,'mm')); print(s)
        BeamSection_Rectangle(Width= 200.000 mm (Distance), Hight= 300.000 mm (Distance), width= 175.000 mm (Distance), hight= 275.000 mm (Distance))
        >>> A = s.A; _ = A.set_displayUnit('cm^2'); print(A)
         119     cm^2 (Area)
        >>> print(s.Ix)
        14700     cm^4 (MomentOfAreaSecond)
        >>> print(s.Iy)
        7720     cm^4 (MomentOfAreaSecond)
        >>> print(s.Jz)
        22400     cm^4 (MomentOfAreaSecond)
        >>> print(s.Wbx)
         978     cm^3 (SectionModulus)
        >>> print(s.Wby)
         772     cm^3 (SectionModulus)
        >>> print(s.Wp)
         621     cm^3 (SectionModulus)

    @note: this assume an ideal rectangle, the values of an rectangle beam are a little bit less than this values!

    """

    def __init__(self, Width, Hight, width=None, hight=None, thickness=None, **varargsd):
        """ """
        # alternative names
        if width is None: varargsd.get('b', None)
        if width is None: varargsd.get('w', None)
        if hight is None: varargsd.get('h', None)
        if thickness is None: varargsd.get('s', None)
        if thickness is None: varargsd.get('t', None)
        #
        Width = ETQ.Distance(Width)
        Hight = ETQ.Distance(Hight)
        if width is not None: width = ETQ.Distance(width)
        if hight is not None: hight = ETQ.Distance(hight)
        if thickness is not None: thickness = ETQ.Distance(thickness)
        if thickness is not None:
            if width is None and hight is None:
                width = ETQ.Distance(Width.uval - 2.0*thickness.uval)
                hight = ETQ.Distance(Hight.uval - 2.0*thickness.uval)
            else:
                raise Exception()
        if width is None:
            width = ETQ.Distance(0.0, 'm')
        if hight is None:
            hight = ETQ.Distance(0.0, 'm')
        #
        self.Width = Width
        self.Hight = Hight
        self.width = width
        self.hight = hight

    def __str__(self):
        return f"BeamSection_Rectangle(Width={self.Width}, Hight={self.Hight}, width={self.width}, hight={self.hight})"

    def A(self):
        """area of section"""
        return ETQ.Area(self.Width.uval*self.Hight.uval - self.width.uval*self.hight.uval)
    A = property(fget=A)

    def Ix(self):
        """moment of inertia of an area about x axis: Ix, Ibx"""
        return ETQ.MomentOfAreaSecond((self.Width.uval*self.Hight.uval**3 - self.width.uval*self.hight.uval**3)/12.0)
    Ix = property(fget=Ix)

    def Iy(self):
        """moment of inertia of an area about y axis: Iy, Iby"""
        return ETQ.MomentOfAreaSecond((self.Width.uval**3*self.Hight.uval - self.width.uval**3*self.hight.uval)/12.0)
    Iy = property(fget=Iy)

    def Jz(self):
        """??? polar moment of inertia of an area: J_z, I_p, J_t"""
        return self.Ix + self.Iy

    Jz = property(fget=Jz)

    def Zex(self):
        """Zex .. elastic section modulus about axis x; Wbx .. Widerstandsmoment um die Achse x"""
        return ETQ.SectionModulus(self.Ix.uval / (self.Hight.uval/2.0))
    Wbx = property(fget=Zex)
    Zex = property(fget=Zex)

    def Zey(self):
        """Zey .. elastic section modulus about axis y; Wby .. Widerstandsmoment um die Achse y"""
        return ETQ.SectionModulus(self.Iy.uval / (self.Width.uval/2.0))
    Wby = property(fget=Zey)
    Zey = property(fget=Zey)

    def Zez(self):
        """??? Zez .. polar elastic section modulus about axis z; Wp .. TrosionsWiderstandsmoment um die Achse z"""
        return ETQ.SectionModulus(self.Jz.uval / ((self.Width.uval**2 + self.Hight.uval**2 ))**(1, 2))
    Wp = property(fget=Zez)
    Zez = property(fget=Zez)


class BeamSection_Pipe(BeamSection):
    """cross-section of a Pipe

    see: L{BeamSection}

        >>> ETQ.Quantity.set_displayUnitSystem('mechanicalEngineering')
        >>> ETQ.Quantity.set_str_quantization(None)
        >>> s = BeamSection_Pipe(ETQ.Distance(0.150, 'm')); print(s)
        BeamSection_Pipe(D= 150.000 mm (Distance), d=   0.000 mm (Distance))
        >>> s = BeamSection_Pipe(ETQ.Distance(0.150, 'm'), ETQ.Distance(0.120, 'm')); print(s)
        BeamSection_Pipe(D= 150.000 mm (Distance), d= 120.000 mm (Distance))
        >>> s = BeamSection_Pipe(ETQ.Distance(200.0, 'mm'), thickness=ETQ.Distance(16.0,'mm')); print(s)
        BeamSection_Pipe(D= 200.000 mm (Distance), d= 168.000 mm (Distance))
        >>> print(s.A)
        9250     mm^2 (Area)
        >>> print(s.Ix)
        3940     cm^4 (MomentOfAreaSecond)
        >>> print(s.Iy)
        3940     cm^4 (MomentOfAreaSecond)
        >>> print(s.Jz)
        7890     cm^4 (MomentOfAreaSecond)
        >>> print(s.Wx)
         394     cm^3 (SectionModulus)
        >>> print(s.Wy)
         394     cm^3 (SectionModulus)
        >>> print(s.Wp)
         789     cm^3 (SectionModulus)

    """

    def __init__(self, D, d=None, thickness=None):
        D = ETQ.Distance(D)
        if d is not None: d = ETQ.Distance(d)
        if thickness is not None: thickness = ETQ.Distance(thickness)
        if d is None and thickness is not None:
            d = ETQ.Distance(D.uval - 2.0*thickness.uval)
        if d is None:
            d = ETQ.Distance(0.0, 'm')
        if d.get_value() >= D.get_value():
            raise functions.EngineeringTools_tools_Error('d >= D')
        self.Diameter = D
        self.diameter = ETQ.Distance(d)

    def __str__(self):
        return f"BeamSection_Pipe(D={self.Diameter}, d={self.diameter})"

    def A(self):
        """area of section"""
        return ETQ.Area((self.Diameter.uval**2-self.diameter.uval**2)*ETQ.PI/4.0)
    A = property(fget=A)

    def Ix(self):
        """moment of inertia of an area about x axis: Ix, Iy, Ibx, Iby"""
        return ETQ.MomentOfAreaSecond((self.Diameter.uval**4-self.diameter.uval**4)*ETQ.PI/64.0)
    Iy = property(fget=Ix)
    Ix = property(fget=Ix)

    def Jz(self):
        """polar moment of inertia of an area: J_z, I_p, J_t"""
        return ETQ.MomentOfAreaSecond((self.Diameter.uval**4-self.diameter.uval**4)*ETQ.PI/32.0)

    Jz = property(fget=Jz)

    def Zex(self):
        """Zex, Zey .. elastic section modulus about axis x,y; Wbx, Wby .. Widerstandsmoment um die Achse x, y"""
        return ETQ.SectionModulus(self.Ix.uval / (self.Diameter.uval/2.0))
    Wx  = property(fget=Zex)
    Wy  = property(fget=Zex)
    Zey = property(fget=Zex)
    Zex = property(fget=Zex)

    def Zez(self):
        """Zez .. polar elastic section modulus about axis z; Wp .. TrosionsWiderstandsmoment um die Achse z"""
        return ETQ.SectionModulus(self.Jz.uval / (self.Diameter.uval/2.0))
    Wp  = property(fget=Zez)
    Zez = property(fget=Zez)



################################################################################
# test
################################################################################
def _setup_doctest():
    ETQ.Quantity.set_displayUnitSystem('mechanicalEngineering')

#eof ###########################################################################


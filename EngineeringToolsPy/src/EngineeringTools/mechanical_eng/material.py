#!/usr/bin/env python3
# pylint: disable-msg=line-too-long,

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"

# run doctest, workaround relative import
if __name__ == '__main__':
    import sys
    import doctest # pylint: disable=import-outside-toplevel
    module_name = 'EngineeringTools.mechanical_eng.material'     # pylint: disable=invalid-name
    module = __import__(module_name, fromlist=['*'], level=0)  # pylint: disable=invalid-name
    module._setup_doctest()                                    # pylint: disable=protected-access
    print(doctest.testmod(module, optionflags=doctest.ELLIPSIS))
    sys.exit()


from .. import quantities as ETQ


class Material:

    def __init__(self):
        self.name = 'material'
        self.identifiers = []
        self.density = None
        self.youngs_modulus = None


    def _repr_html_(self):
        html = f"""<h2>{self.name}</h2>
<table border="1">\n

    <tr>
        <td colspan="2" style="text-align:left">{self.__class__.__module__+'.'+self.__class__.__name__}</td>
    </tr>
    <tr>
        <td>identifiers:</td>
        <td style="text-align:left">{self.identifiers}</td>
    </tr>
    <tr>
        <td>density:</td>
        <td style="text-align:left">{self.density._repr_html_()}</td>
    </tr>
    <tr>
        <td>young's modulus:</td>
        <td style="text-align:left">{self.youngs_modulus._repr_html_()}</td>
    </tr>    
</table>
"""
        return html



    def __str__(self):
        return """{name}
name:           {self.name}
identifiers:    {self.identifiers}
density:        {self.density}
youngs modulus: {self.youngs_modulus}  
""".format(self=self, name=self.__class__.__module__+'.'+self.__class__.__name__)

    #__repr__ = __str__



class Steel(Material):

    def __init__(self):
        super(Steel, self).__init__()
        self.name = 'steel'
        self.density = ETQ.Density(7800., 'kg/m3')
        self.youngs_modulus = ETQ.Stress(210e3, 'N/mm2')
        self.shear_modulus =  ETQ.Stress( 80e3, 'N/mm2')
        self.Rp_list = []
        self.thermal_expansion_coefficient_linear = ETQ.ThermalExpansionCoefficientLinear(12e-6, '1/K')

    def Rp(self, thicknessNominal=None):
        # TODO: implement search in list
        return self.Rp_list[0]



class Steel_S355JR(Steel):
    '''
    http://www.steelnumber.com/en/steel_composition_eu.php?name_id=8
    '''

    def __init__(self):
        """ """
        super(Steel_S355JR, self).__init__()
        self.name = 'Steel: S355JR'
        self.identifiers.append('S355JR')
        self.identifiers.append('1.0045')
        self.identifiers.append('St52-3')
        self.identifiers.append('Sweden SS 2132-01')
        self.Rp_list = [ETQ.Stress(355., 'N/mm2'),
                        ETQ.Stress(345., 'N/mm2'),
                        ETQ.Stress(335., 'N/mm2'),
                        ETQ.Stress(325., 'N/mm2'),
                        ETQ.Stress(295., 'N/mm2'),
                        ETQ.Stress(285., 'N/mm2'),
                        ETQ.Stress(275., 'N/mm2')]


class Steel_34CrNiMo6(Steel):

    def __init__(self):
        super(Steel_34CrNiMo6, self).__init__()
        self.name = 'Steel: 34CrNiMo6'
        self.identifiers.append('34CrNiMo6')
        self.identifiers.append('1.6582')
        self.identifiers.append('Sweden SS 2541')
        self.Rp_list = [ETQ.Stress(1000., 'N/mm2'),
                       ]

class CastIron(Material):
    """https://www.meuselwitz-guss.de/fileadmin/daten/Dateien/pdf/werkstoffe/Werkstoffkenndaten_Lammellengraphit.pdf"""

    def __init__(self):
        """ """
        super(CastIron, self).__init__()
        self.name = 'CastIron: EN - GJL'
        self.density = ETQ.Density(7200., 'kg/m3')
        self.youngs_modulus = ETQ.Stress(110e3, 'N/mm2')
        self.thermal_expansion_coefficient_linear = ETQ.ThermalExpansionCoefficientLinear(12e-6, '1/K')
        self.heat_capacity_specific = ETQ.HeatCapacitySpecific(0.46, 'kJ/(kg.K)')

class ChilledDuctileIron_CDI580(CastIron):
    """Chilled Ductile Iron
    https://www.hwk1365.de/en/cdi/"""

    def __init__(self):
        """ """
        super(ChilledDuctileIron_CDI580, self).__init__()
        self.name = 'Chilled Ductile Iron: Cast_CDI580'
        self.identifiers.append('CDI 580')
        self.density = ETQ.Density(7200., 'kg/m3')
        self.youngs_modulus = ETQ.Stress(175000, 'N/mm2')
        self.thermal_expansion_coefficient_linear = ETQ.ThermalExpansionCoefficientLinear(12.5e-6, '1/K')
        #self.heatCapacitySpecific = ETQ.HeatCapacitySpecific(, '')
        self.ultimate_tensile_strength = ETQ.Stress(700, 'N/mm2')
        self.yield_strength = ETQ.Stress(440, 'N/mm2')
        self.thermal_conductivity = ETQ.ThermalConductivity(35, 'W/(m.K)')
        #self.poissons_ratio     # FIXME


################################################################################
# test
################################################################################
def _setup_doctest():
    ETQ.Quantity.set_displayUnitSystem('mechanicalEngineering')

# eof

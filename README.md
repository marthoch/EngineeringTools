# EngineeringTools

EngineeringTools supports engineering calculations by providing quantities (like Distance, Volume, Area, Force, ..).  
Quantities provide ways for user readable input with unit conversion and engineering like formatted output. Inconsistency with units and quantities is a common problem in engineering calcualtions.  
Quantities provide automatic unit checking in calculations and so supporting engineers to avoid mistakes in calculations.   
EngineeringTools provides tools supporting engineers like beam section calculations, fluid power, and so on. 


```python
# Example: Calculation of the Volume of a Box
>>> data = ET.Obj('Box')
>>> data.length = ET.Distance(150, 'mm')
>>> data.width  = ET.Distance( 50, 'mm')
>>> data.hight  = ET.Distance( 75, 'mm')
>>> data
Box
length	       150.000 mm (Distance)
width	        50.000 mm (Distance)
hight	        75.000 mm (Distance)

>>> ET.Volume(data.length * data.width * data.hight)
      562     cm3 (Volume)
      
>>> ET.Area(data.length * data.width * data.hight)  # shall fail
EngineeringTools_uval_Error               Traceback (most recent call last)
EngineeringTools_uval_Error: units do not match: {'meter': Fraction(3, 1)} != {'meter': 2}

>>> A = ET.Area(data.length * data.width)
>>> A
      7 500     mm^2 (Area)

```


## Totorial

[EngineeringToolsPy/NoteBooks/Examples.ipynb](EngineeringToolsPy/NoteBooks/Examples.ipynb)


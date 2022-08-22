# EngineeringTools

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


Query Examples
============================

Areas by surfaceType
--------------------

This query calculates the total area for each surfaceType.

.. code-block:: python

   from lxml import etree
   import xgbxml

   parser = xgbxml.get_parser('0.37')   

   tree = etree.parse('gbXMLStandard.xml', parser)  # file available on GitHub here: https://github.com/GreenBuildingXML/Sample_gbXML_Files
   gbxml = tree.getroot()

   result = {}
   for surface in gbxml.Campus.Surfaces:
    
       surface_type = surface.surfaceType
    
       try:  
           surface_plus_openings_area = surface.PlanarGeometry.get_area()  # this raises an error in a few cases as the polygon in the 'gbXMLStandard.xml' file has three adjacent vertices on a line.
       except ValueError:
           print(f'Error raised for get_area() of Surface {surface.id}')
           continue
    
       x = result.setdefault(surface_type,0)
       result[surface_type] = x + surface_plus_openings_area
    
   print(result)
   # prints "{'ExteriorWall': 38663.957965668895, 
   #          'Shade': 3602.1242386749996, 
   #          'InteriorWall': 59075.35491038435, 
   #          'InteriorFloor': 71901.632959902, 
   #          'Ceiling': 2041.1025198133002, 
   #          'Roof': 20895.388879540173, 
   #          'SlabOnGrade': 19542.64927603096}"



Areas and window-to-wall ratio by orientation
---------------------------------------------

This query calculates the opening, surface and total areas, and the window-to-wall ratio for each orientation of the surfaces.

.. code-block:: python

   from lxml import etree
   import xgbxml

   parser=xgbxml.get_parser('0.37')   

   tree=etree.parse('gbXMLStandard.xml', parser)  # file available on GitHub here: https://github.com/GreenBuildingXML/Sample_gbXML_Files
   gbxml=tree.getroot()

   result={}
   for surface in gbxml.Campus.Surfaces:
    
       cad_model_azimuth = gbxml.Campus.Location.CADModelAzimuth.value
       surface_azimuth = surface.RectangularGeometry.Azimuth.value
       orientation = cad_model_azimuth + surface_azimuth
    
       try:
           total_area=surface.PlanarGeometry.get_area()  # this raises an error in a few cases as the polygon in the 'gbXMLStandard.xml' file has three adjacent vertices on a line.
           surface_area=surface.get_area()  # this raises an error in a few cases as the polygon in the 'gbXMLStandard.xml' file has three adjacent vertices on a line.
       except ValueError:
           print(f'Error raised for get_area() of Surface {surface.id}')
           continue
        
       opening_area = total_area - surface_area   
    
       x=result.setdefault(orientation,
                           {'opening_area':0,
                            'surface_area':0,
                            'total_area':0}
                          )
       x['opening_area']+=opening_area
       x['surface_area']+=surface_area
       x['total_area']+=total_area
    
   for k,v in result.items():
       result[k]['window_to_wall_ratio']=result[k]['opening_area'] / result[k]['total_area']
    
   result = dict(sorted(result.items()))  # sorts the dictionary by key
    
   print(result)
   # prints "{0.0: {'opening_area': 1054.302770011667, 
   #                'surface_area': 39379.89112896028, 
   #                'total_area': 40434.19389897194, 
   #                'window_to_wall_ratio': 0.026074534159031996}, 
   #         0.01: {'opening_area': 0.0, 
   #                'surface_area': 18.75935256182059, 
   #                'total_area': 18.75935256182059, 
   #                'window_to_wall_ratio': 0.0}, 
   #         ...
   #         }
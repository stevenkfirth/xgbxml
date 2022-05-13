How do I open a gbXML file?
===========================

Opening a gbXML file using lxml
-------------------------------

gbXML files can be `opened using the standard lxml process <https://lxml.de/tutorial.html#parsing-from-strings-and-files>`_ as follows:

.. code-block:: python

   from lxml import etree

   tree=etree.parse('gbXMLStandard.xml')
   gbxml=tree.getroot()

   print(type(gbxml))        
   # prints "<class 'lxml.etree._Element'>"

   print(len(list(gbxml)))   
   # prints "1159" 

   print (gbxml.attrib)      
   # prints "{'useSIUnitsForResults': 'false', 'temperatureUnit': 'C', 'lengthUnit': 'Feet', 
   #          'areaUnit': 'SquareFeet', 'volumeUnit': 'CubicFeet', 'version': '0.37'}"
   
Opening a gbXML file using xgbxml
---------------------------------

When using *xgbxml*, a parser is first created using the :py:func:`~xgbxml.xgbxml.get_parser` function. 

This parser is then used by *lxml* when parsing the gbXML file.


.. code-block:: python

   from lxml import etree
   import xgbxml

   parser=xgbxml.get_parser('0.37')   

   tree=etree.parse('gbXMLStandard.xml', parser)
   gbxml=tree.getroot()

   print(type(gbxml))        
   # prints "<class 'xgbxml.xgbxml.gbXML'>"

   print(len(list(gbxml)))   
   # prints "1159" 

   print (gbxml.attrib)      
   # prints "{'useSIUnitsForResults': 'false', 'temperatureUnit': 'C', 'lengthUnit': 'Feet', 
   #          'areaUnit': 'SquareFeet', 'volumeUnit': 'CubicFeet', 'version': '0.37'}"
	
Note that the :code:`gbxml` variable is now an instance of the :code:`xgbxml.xgbxml.gbXML` class. This is a class provided by *xgbxml* which extends the :code:`lxml.etree._Element` class with additional attributes and methods.
	
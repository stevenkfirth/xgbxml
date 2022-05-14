How do I edit a gbXML file?
===========================

Editing a gbXML file using lxml
-------------------------------

A gbXML file can be edited using the `standard properties of the lxml Element class <https://lxml.de/tutorial.html#the-element-class>`_.

.. code-block:: python

   from lxml import etree

   tree=etree.parse('gbXMLStandard.xml')
   gbxml=tree.getroot()

   # edit an attribute
   gbxml.attrib['temperatureUnit']='F'
   print(gbxml.attrib['temperatureUnit'])  
   # prints "F"

   # add a child node
   new_node=etree.SubElement(gbxml,'{http://www.gbxml.org/schema}Construction')
   print(new_node.tag)  
   # prints "{http://www.gbxml.org/schema}Construction"

   # edit node text
   gbxml[0][0][0].text = 'my_new_station_id'
   print(gbxml[0][0][0].text)
   # prints "my_new_station_id"

Note the final edit changes the text of the 'StationId' element, located in 'gbXML/Camus/Location'.


Additional editing methods provided by xgbxml
---------------------------------------------

In *xgbxml*, new element properties are available to edit gbXML elements. In particular, the :code:`add_Construction()` method shown below automatically creates a child Construction element on the gbXML element.


.. code-block:: python

   from lxml import etree
   import xgbxml

   parser=xgbxml.get_parser('0.37')   

   tree=etree.parse('gbXMLStandard.xml', parser)
   gbxml=tree.getroot()

   # edit an attribute
   gbxml.temperatureUnit='F'
   print(gbxml.temperatureUnit)  
   # prints "F"

   # add a child node
   new_node=gbxml.add_Construction()
   print(new_node.tag)  
   # prints "{http://www.gbxml.org/schema}Construction"

   # edit node text
   gbxml.Campus.Location.StationId.text = 'my_new_station_id'
   print(gbxml.Campus.Location.StationId.text)
   # prints "my_new_station_id"
   
   
Saving the gbXML file
---------------------

This is done with the standard *lxml* process using the :code:`write` method of the *etree* instance.

.. code-block:: python

   from lxml import etree
   import xgbxml

   parser=xgbxml.get_parser('0.37')   

   tree=etree.parse('gbXMLStandard.xml', parser)
   gbxml=tree.getroot()

   # edit an attribute
   gbxml.temperatureUnit='F'

   # save the edited file
   tree.write('edited_gbxml_file.xml')










   
   
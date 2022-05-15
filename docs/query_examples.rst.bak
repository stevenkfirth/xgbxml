How do I query a gbXML file?
============================

Querying a gbXML file using lxml
--------------------------------

A gbXML file can be queried using the `standard properties of the lxml Element class <https://lxml.de/tutorial.html#the-element-class>`_.


.. code-block:: python

   from lxml import etree

   tree=etree.parse('gbXMLStandard.xml')
   gbxml=tree.getroot()

   # query an attribute
   print(gbxml.attrib['version'])  
   # prints "0.37"

   # query a child element
   print(gbxml[0].tag)
   # prints "{http://www.gbxml.org/schema}Campus"

   # query element text
   print(gbxml[0][0][0].text)
   # prints "52939_2004"

Note the final query is the text for the 'StationId' element, located in 'gbXML/Camus/Location'.


Querying a gbXML file using XPATH
---------------------------------

gbXML files opened in *lxml* can also be queried using `XPATH <https://lxml.de/xpathxslt.html>`_.

.. code-block:: python

   from lxml import etree

   tree=etree.parse('gbXMLStandard.xml')
   gbxml=tree.getroot()

   ns={'gbxml':'http://www.gbxml.org/schema'}

   # query an attribute
   print(gbxml.xpath('./@version')[0])  
   # prints "0.37"

   # query a child element
   print(gbxml.xpath("./gbxml:*", namespaces=ns)[0].tag)
   # prints "{http://www.gbxml.org/schema}Campus"

   # query element text
   print(gbxml.xpath(".//gbxml:StationId/text()", namespaces=ns)[0])
   # prints "52939_2004"


Additional querying methods provided by xgbxml
----------------------------------------------

In *xgbxml*, additional properties are available to query the gbXML file:

.. code-block:: python

   from lxml import etree
   import xgbxml

   parser=xgbxml.get_parser('0.37')   

   tree=etree.parse('gbXMLStandard.xml', parser)
   gbxml=tree.getroot()

   # query an attribute
   print(gbxml.version)  
   # prints "0.37"

   # query a child element
   print(gbxml.Campus.tag)
   # prints "{http://www.gbxml.org/schema}Campus"

   # query element text
   print(gbxml.Campus.Location.StationId.text)
   # prints "52939_2004"
   
The additional properties that *xgbxml* supplies include:

- attributes for accessing gbXML element attributes (i.e. :code:`version`)
- attributes for accessing gbXML child elements (i.e. :code:`Campus`)

Advanced querying using xgbxml
------------------------------

*xgbxml* attributes can query for multiple child elements (i.e. :code:`gbxml.Campus.Surfaces`). 

These can also be nested (i.e. :code:`gbxml.Campus.Surfaces.Openings`).

.. code-block:: python

   from lxml import etree
   import xgbxml

   parser=xgbxml.get_parser('0.37')   

   tree=etree.parse('gbXMLStandard.xml', parser)
   gbxml=tree.getroot()

   print(len(gbxml.Campus.Surfaces))
   # prints "2590"

   print(len(gbxml.Campus.Surfaces.Openings))
   # prints "138"

This shows that the gbXML file has 2,590 surfaces and 138 openings.
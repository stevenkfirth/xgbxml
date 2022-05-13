How do I create a new gbXML file?
=================================

Using the `create_gbxml` function
---------------------------------

The :py:func:`~xgbxml.xgbxml.create_gbXML` function is used to create a new :code:`xgbxml.xgbxml.gbXML` instance.

.. code-block:: python

   import xgbxml
   gbxml=xgbxml.create_gbXML()

   print(type(gbxml))
   # prints "<class 'xgbxml.xgbxml.gbXML'>"

   print(gbxml.tostring())
   # prints "<gbXML xmlns="http://www.gbxml.org/schema" version="6.01" temperatureUnit="C" 
   #                lengthUnit="Meters" areaUnit="SquareMeters" volumeUnit="CubicMeters" 
   #                useSIUnitsForResults="true"/>

   print(type(gbxml.getroottree()))
   # prints "<class 'lxml.etree._ElementTree'>"

Note, to access the element tree the lxml method :code:`getroottree` can be used.


Adding more elements
--------------------

What extra methods does xgbxml provide?
=======================================

Viewing methods on xgbxml elements
----------------------------------

Each gbXML element in xgbxml has a number of methods and properties.

The are a combination of:

- Properties and methods inherited from lxml etree.Element (as xgbxml is an extension of lxml).
- Properties and methods inherited from the :py:class:`~xgbxml.xgbxml.gbElement` class.
- Properties and methods that are automatically generated from the gbXML schema file. For example, this method generates the :code:`version` property and the :code:`add_Campus` method for the gbXML element.
  *Please note that the schema-generated methods and properties are not listed in documentation, as the gbXML schema is a large schema and listing each method and property is impractical as there are too many*.
- Properties and methods which are custom written for the element. This is bespoke code written for a particular element to provide additional functionality. An example is the 
  :py:func:`~xgbxml.xgbxml.Surface.get_shell` method of the :py:class:`~xgbxml.xgbxml.Surface` class.

To view these methods for a particular element, a call to the python built-in function :code:`dir` can be used.
In the example below, the methods and properties of the *gbXML* element are displayed.

.. code-block:: python

   import xgbxml
   gbxml=xgbxml.create_gbXML()

   print([x for x in dir(gbxml) if not x.startswith('_')])
   # prints "['AirLoop', 'AirLoops', 'Campus', 'Campuss', 'Construction', 'Constructions', 'DaySchedule', 'DaySchedules', 'DocumentHistory', 'DocumentHistorys', 'ExtEquip', 'ExtEquips', 'HydronicLoop', 'HydronicLoops', 'IntEquip', 'IntEquips', 'Layer', 'Layers', 'LightingControl', 'LightingControls', 'LightingSystem', 'LightingSystems', 'Material', 'Materials', 'Meter', 'Meters', 'Results', 'Resultss', 'Schedule', 'Schedules', 'SimulationParameters', 'SimulationParameterss', 'SurfaceReferenceLocation', 'Weather', 'Weathers', 'WeekSchedule', 'WeekSchedules', 'WindowType', 'WindowTypes', 'Zone', 'Zones', 'add_AirLoop', 'add_Campus', 'add_Construction', 'add_DaySchedule', 'add_DocumentHistory', 'add_ExtEquip', 'add_HydronicLoop', 'add_IntEquip', 'add_Layer', 'add_LightingControl', 'add_LightingSystem', 'add_Material', 'add_Meter', 'add_Results', 'add_Schedule', 'add_SimulationParameters', 'add_Weather', 'add_WeekSchedule', 'add_WindowType', 'add_Zone', 'add_aecXML', 'add_child', 'addnext', 'addprevious', 'aecXML', 'aecXMLs', 'append', 'areaUnit', 'attrib', 'base', 'clear', 'cssselect', 'engine', 'extend', 'find', 'findall', 'findtext', 'get', 'get_attribute', 'get_attributes', 'get_child', 'get_children', 'getchildren', 'getiterator', 'getnext', 'getparent', 'getprevious', 'getroottree', 'id', 'index', 'insert', 'items', 'iter', 'iterancestors', 'iterchildren', 'iterdescendants', 'iterfind', 'itersiblings', 'itertext', 'keys', 'lengthUnit', 'makeelement', 'nntag', 'ns', 'nsmap', 'prefix', 'remove', 'replace', 'set', 'set_attribute', 'sourceline', 'tag', 'tail', 'temperatureUnit', 'text', 'tostring', 'useSIUnitsForResults', 'value', 'values', 'version', 'volumeUnit', 'xpath', 'xsd_schema']"

Schema-based automatically-generated methods and properties
-----------------------------------------------------------

Depending on the version used in the *xgbxml* parser, a series of automatically-generated methods and properties are created based on the schema for that version.

These methods and properties are useful for working with child elements and XML attributes.

For example, according to the schema the *gbXML* element can have *AirLoop* child elements. As such, the *gbXML* element in *xgbxml* contains:

- the :code:`AirLoop` property, which returns the first *AirLoop* child element found (uses :py:func:`~xgbxml.xgbxml.gbElement.get_child`).
- the :code:`AirLoops` property (named by appending a "s" to the child element name), which returns all the *AirLoop* child elements (uses :py:func:`~xgbxml.xgbxml.gbElement.get_children`).
- the :code:`add_AirLoop()` method, which is useful for creating new AirLoop child elements (uses :py:func:`~xgbxml.xgbxml.gbElement.add_child`).

Similarly, according to the schema the *gbXML* element can have a *temperatureUnit* XML attribute. As such, the *gbXML* element in *xgbxml* contains:

- the :code:`temperatureUnit` property, which can be used to return and set the *temperatureUnit* attribute (uses :py:func:`~xgbxml.xgbxml.gbElement.get_attribute`
  and :py:func:`~xgbxml.xgbxml.gbElement.set_attribute`).





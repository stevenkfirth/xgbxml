What is xgbxml?
===============

*xgbxml* is an extension for the well-known python package *lxml* https://lxml.de/.

*lxml* is a Python processor for XML files and comes with Anaconda distribution as standard.

*xgbxml* extends *lxml* for working with gbXML files. gbXML (Green Building XML, https://www.gbxml.org/) is an XML format for sharing information about buildings, often for the purposes of energy simulation.

It would be entirely possible to work with gbXML files using *lxml* alone. However *xgbxml* provides additional methods and features that make working with gbXML much quicker and easier.

The source code for *xgbxml* is on GitHub here: https://github.com/stevenkfirth/xgbxml

..
  A standard way to work with XML files with Python is to use the python library *lxml* https://lxml.de/.
  In the *lxml* documentation, there is a section on `Using custom Element classes in lxml <https://lxml.de/element_classes.html>`_. 
  This describes how the standard classes in lxml can be extended to include custom methods and properties.
  *xgbxml* (this package) uses these custom element classes to provide a more user-friendly way of using *lxml* to work with gbXML files. 
  By using the parser provided by *xgbxml*, a user gains access to additional methods and functions to read, edit and create gbXML files and elements.


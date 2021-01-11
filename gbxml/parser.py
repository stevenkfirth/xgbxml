# -*- coding: utf-8 -*-

from .gbXML import gbXML

from .gbxmlElement import gbxmlElement

from lxml import etree

ns='http://www.gbxml.org/schema'

lookup = etree.ElementNamespaceClassLookup()
parser = etree.XMLParser()
parser.set_element_class_lookup(lookup)
namespace = lookup.get_namespace(ns)

namespace[None]=gbxmlElement

# loops through all globals and adds any etree.ElementBase subclasses to namespace
for k,v in list(globals().items()):
    
    try:
    
        #if v.__base__==etree.ElementBase:
        if v.__base__==gbxmlElement:
            
        
            namespace[k]=v
        
    except AttributeError:
        
        pass
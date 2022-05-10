# -*- coding: utf-8 -*-
"""
Created on Mon May  9 12:02:05 2022

@author: cvskf
"""

import unittest

from xgbxml.xsd_functions import *

from lxml import etree

from copy import copy

fp=r'files/GreenBuildingXML_Ver6.01.xsd'
tree=etree.parse(fp)
xml_schema=tree.getroot()


class Test_xsd_attribute(unittest.TestCase):
    ""
    
    def test_get_type_from_xsd_attribute(self):
        ""
        gbxml=get_xsd_element_from_xsd_schema(xml_schema,
                                              'gbXML')
        
        id_=get_xsd_attribute_from_xsd_element(gbxml,
                                             'id')
        self.assertEqual(get_type_from_xsd_attribute(id_),
                         'xsd:ID')
        
        engine=get_xsd_attribute_from_xsd_element(gbxml,
                                                  'engine')
        x=get_type_from_xsd_attribute(engine)
        self.assertEqual(x.tag,
                         '{http://www.w3.org/2001/XMLSchema}simpleType')
        self.assertEqual(engine.attrib['name'],
                         'engine')


class Test_xsd_schema(unittest.TestCase):
    ""
    
    def test_get_xsd_element_from_xsd_schema(self):
        ""
        x=get_xsd_element_from_xsd_schema(xml_schema,
                                          'Coordinate')
        self.assertEqual(x.attrib['name'],
                         'Coordinate')
        
        
class Test_xsd_element(unittest.TestCase):
    ""
    
    def test_get_xsd_attribute_from_xsd_element(self):
        ""
        gbxml=get_xsd_element_from_xsd_schema(xml_schema,
                                              'gbXML')
        id_=get_xsd_attribute_from_xsd_element(gbxml,
                                             'id')
        self.assertEqual(id_.attrib['name'],
                         'id')
        
        
    def test_get_xsd_attribute_names_from_xsd_element(self):
        ""
        gbxml=get_xsd_element_from_xsd_schema(xml_schema,
                                              'gbXML')
        self.assertEqual(get_xsd_attribute_names_from_xsd_element(gbxml),
                         ['id', 
                          'engine', 
                          'temperatureUnit', 
                          'lengthUnit', 
                          'areaUnit', 
                          'volumeUnit', 
                          'useSIUnitsForResults', 
                          'version', 
                          'SurfaceReferenceLocation'])
        
        
        
        
class Test_xsd_simpleType(unittest.TestCase):
    ""
    
    def test_get_restriction_base_from_xsd_simple_type(self):
        ""
        gbxml=get_xsd_element_from_xsd_schema(xml_schema,
                                              'gbXML')
        engine=get_xsd_attribute_from_xsd_element(gbxml,
                                                  'engine')
        simple_type=get_type_from_xsd_attribute(engine)
        self.assertEqual(get_restriction_base_from_xsd_simple_type(simple_type),
                         'xsd:NMTOKEN')
        
    
    def test_get_restriction_enumeration_values_from_xsd_simple_type(self):
        ""
        gbxml=get_xsd_element_from_xsd_schema(xml_schema,
                                              'gbXML')
        engine=get_xsd_attribute_from_xsd_element(gbxml,
                                                  'engine')
        simple_type=get_type_from_xsd_attribute(engine)
        self.assertEqual(get_restriction_enumeration_values_from_xsd_simple_type(simple_type),
                         ['DOE2.1e', 'DOE2.2', 'EnergyPlus'])
        
        
if __name__=='__main__':
    
    unittest.main()
    
    


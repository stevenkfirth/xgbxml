# -*- coding: utf-8 -*-
"""
Created on Mon May  9 09:39:02 2022

@author: cvskf
"""

import unittest

from lxml import etree

from xgbxml.gbxml_functions import *


fp=r'files\gbXMLStandard.xml'
tree = etree.parse(fp)
gbxml=tree.getroot()
ns={'gbxml':'http://www.gbxml.org/schema'}

cp=gbxml.xpath('//gbxml:CartesianPoint', namespaces=ns)[0]  # first CartesianPoint


fp=r'files\GreenBuildingXML_Ver6.01.xsd'
xsd_schema = etree.parse(fp).getroot()


class Test_common(unittest.TestCase):
    ""
    
    def test_set_attribute(self):
        ""
        xml='<gbXML version="6.01" xmlns="http://www.gbxml.org/schema"></gbXML>' 
        gbxml=etree.fromstring(xml)  # root node
        set_attribute_on_gbxml_element(gbxml_element=gbxml,
                                       attribute_name='temperatureUnit',
                                       value='C',
                                       xsd_schema=xsd_schema)
        self.assertEqual(gbxml.attrib,
                         {'version': '6.01', 'temperatureUnit': 'C'})


class Test_CartesianPoint(unittest.TestCase):
    ""
    
    
    def test_get_coordinate_values_from_CartesianPoint(self):
        ""
        x=get_coordinate_values_from_CartesianPoint(cp, 
                                                    xsd_schema)
        self.assertEqual(x,
                         (47.90424, 58.64111, 474.0))
        
        
        
if __name__=='__main__':
    
    unittest.main()
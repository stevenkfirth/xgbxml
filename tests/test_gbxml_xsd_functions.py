# -*- coding: utf-8 -*-
"""
Created on Mon May  9 15:54:28 2022

@author: cvskf
"""

import unittest

from xgbxml.gbxml_xsd_functions import *

from lxml import etree

from copy import copy

fp=r'files/GreenBuildingXML_Ver6.01.xsd'
tree=etree.parse(fp)
xsd_schema=tree.getroot()
namespace='http://www.gbxml.org/schema'


class Test_xsd_element(unittest.TestCase):
    ""
    
    def test_get_text_type_of_xsd_element(self):
        ""
        self.assertEqual(get_xsd_type_of_text_of_xsd_element(name='Coordinate',
                                                             xsd_schema=xsd_schema),
                         'xsd:decimal')
        
        #print(etree.tostring(copy(x)).decode())
        
        #print(get_xsd_type_from_xsd_element(x).tag)
        
        
        
if __name__=='__main__':
    
    unittest.main()
    
    
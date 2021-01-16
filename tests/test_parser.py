# -*- coding: utf-8 -*-

import unittest

from gbxml import get_parser, create_gbXML
from lxml import etree


class Test_parser(unittest.TestCase):
   
    def test_create_gbXML(self):
        ""
        gbXML=create_gbXML()
        print(gbXML)
        print(gbXML.attributes)
        
    
    
    def test_get_parser(self):
        ""
        fp=r'files\gbXMLStandard.xml'
        
        parser=get_parser(version='0.37')
        print(parser)
        
        tree = etree.parse(fp,parser)
        gbXML=tree.getroot()
        print(gbXML)
        print(gbXML.Campus)
        
    
if __name__=='__main__':
    
    unittest.main(Test_parser())
    
    
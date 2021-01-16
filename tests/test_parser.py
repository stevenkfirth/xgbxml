# -*- coding: utf-8 -*-

import unittest

from gbxml import parser, create_gbXML
from lxml import etree
import gbxml


class Test_parser(unittest.TestCase):
   
    
    def test_parser(self):
        ""
        
        
        
        fp=r'files\gbXMLStandard.xml'
        tree = etree.parse(fp,parser)
        gbXML=tree.getroot()
        
        print(gbXML)
        gbXML.test()
        print(gbXML.Campus)
        
        print(gbXML.Campus.Location.CADModelAzimuth)
        
        
        
        
    # def test_new_gbXML(self):
        
    #     st=gbxml.new_gbXML_string
    #     #print(st)
    #     tree = etree.parse(st,parser)
    #     gbXML=tree.getroot()
    #     #print(gbXML)
    #     gbXML.add_Campus()
    #     #print(etree.tostring(gbXML))
    #     #print(gbXML.Campus)
        
    #     st='<gbXML version="6.01" xmlns="http://www.gbxml.org/schema"></gbXML>'
    #     gbXML=etree.fromstring(st,parser)
    #     #print(gbXML)
        
        
    # def test_create_gbXML(self):
    #     ""
    #     gbXML=create_gbXML()
    #     #print(gbXML)
    #     #print(gbXML.attributes)
        
        
        
        
    
if __name__=='__main__':
    
    unittest.main(Test_parser())
    
    
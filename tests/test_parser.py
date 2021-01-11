# -*- coding: utf-8 -*-


import unittest

from gbxml import parser
from lxml import etree


class Test_parser(unittest.TestCase):
   
    
    def test_parser(self):
        ""
        
        fp=r'files\gbXMLStandard.xml'
        tree = etree.parse(fp,parser)
        gbXML=tree.getroot()
        print(gbXML)
        gbXML.test()
        
        print(gbXML.attrib)
        print(gbXML.get('version'))
        print(gbXML.text)
        print(len(gbXML))
        
        print(gbXML[0])
    
    
if __name__=='__main__':
    
    unittest.main(Test_parser())
    
    
# -*- coding: utf-8 -*-

import unittest

from gbxml import parser
from lxml import etree


class Test_gbXML(unittest.TestCase):
   

    
    
    def test_Campus(self):
        ""
        self.assertEqual(gbXML.Campus.nntag,
                         'Campus')
        
        
    def test_Constructions(self):
        ""
        self.assertEqual(len(gbXML.Constructions),
                         11)
        self.assertEqual(gbXML.Constructions[0].nntag,
                         'Construction')
        
        
    def test_id_(self):
        ""
        gbXML.id_='id0001'
        self.assertEqual(gbXML.id_,
                         'id0001')
    
    
    
    
if __name__=='__main__':
    
    fp=r'files\gbXMLStandard.xml'
    tree = etree.parse(fp,parser)
    gbXML=tree.getroot()
    unittest.main(Test_gbXML())
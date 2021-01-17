# -*- coding: utf-8 -*-

import unittest

from gbxml import create_gbXML
from lxml import etree


class Test_Surface(unittest.TestCase):
   

    def test_get_Campus(self):
        ""
        gbXML=create_gbXML()
        su=gbXML.add_Campus(id='campus1').add_Surface(id='surface1')
        self.assertEqual(su.get_Campus(),
                         gbXML.Campus)


    def test_get_Spaces(self):
        ""
        gbXML=create_gbXML()
        b=gbXML.add_Campus().add_Building()
        sp1=b.add_Space(id='space1')
        sp2=b.add_Space(id='space2')
        su=gbXML.Campus.add_Surface(id='surface1')
        su.add_AdjacentSpaceId(spaceIdRef='space1')
        su.add_AdjacentSpaceId(spaceIdRef='space2')
        
        self.assertEqual(su.get_Spaces(),
                         [sp1,sp2])

        
if __name__=='__main__':
    
    unittest.main(Test_Surface())
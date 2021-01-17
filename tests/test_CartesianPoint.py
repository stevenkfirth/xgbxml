# -*- coding: utf-8 -*-

import unittest

from gbxml import create_gbXML
from lxml import etree


class Test_CartesianPoint(unittest.TestCase):
   

    def test_create_Coordinates(self):
        ""
        coordinates=(10,0,0)
        gbXML=create_gbXML()
        cp=gbXML.add_Campus().add_Building().add_Space().add_PlanarGeometry().add_PolyLoop().add_CartesianPoint()
        cp.create_Coordinates(*coordinates)
        #print(etree.tostring(cp,pretty_print=True).decode())
        
        parser=etree.XMLParser(remove_blank_text=True)
        answer=etree.fromstring("""<CartesianPoint xmlns="http://www.gbxml.org/schema">
                                        <Coordinate>10</Coordinate>
                                        <Coordinate>0</Coordinate>
                                        <Coordinate>0</Coordinate>
                                      </CartesianPoint>
                                     """,
                                parser=parser)
        
        self.assertEqual(etree.tostring(cp),
                         etree.tostring(answer))
        
        
    def test_get_coordinates(self):
        ""
        return
        
        coordinates=(10,0,0)
        gbXML=create_gbXML()
        cp=gbXML.add_Campus().add_Building().add_Space().add_PlanarGeometry().add_PolyLoop().add_CartesianPoint()
        cp.create_coordinates(*coordinate_values)
        
        self.assertEqual(cp.get_coordinates(),
                         coordinates)
        
        
        
if __name__=='__main__':
    
    
    unittest.main(Test_CartesianPoint())
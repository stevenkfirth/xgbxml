# -*- coding: utf-8 -*-

import unittest

from gbxml import create_gbXML
from lxml import etree


class Test_PolyLoop(unittest.TestCase):
   

    def test_create_CartesianPoints(self):
        ""
        points_coordinates=((0,0,0),(10,0,0),(10,10,0),(0,10,0))
        gbXML=create_gbXML()
        pl=gbXML.add_Campus().add_Building().add_Space().add_PlanarGeometry().add_PolyLoop()
        pl.create_CartesianPoints(*points_coordinates)
        #print(etree.tostring(pl,pretty_print=True).decode())
        
        parser=etree.XMLParser(remove_blank_text=True)
        answer=etree.fromstring("""<PolyLoop xmlns="http://www.gbxml.org/schema">
                                      <CartesianPoint>
                                        <Coordinate>0</Coordinate>
                                        <Coordinate>0</Coordinate>
                                        <Coordinate>0</Coordinate>
                                      </CartesianPoint>
                                      <CartesianPoint>
                                        <Coordinate>10</Coordinate>
                                        <Coordinate>0</Coordinate>
                                        <Coordinate>0</Coordinate>
                                      </CartesianPoint>
                                      <CartesianPoint>
                                        <Coordinate>10</Coordinate>
                                        <Coordinate>10</Coordinate>
                                        <Coordinate>0</Coordinate>
                                      </CartesianPoint>
                                      <CartesianPoint>
                                        <Coordinate>0</Coordinate>
                                        <Coordinate>10</Coordinate>
                                        <Coordinate>0</Coordinate>
                                      </CartesianPoint>
                                    </PolyLoop>
                                """,
                                parser=parser)
        
        self.assertEqual(etree.tostring(pl),
                         etree.tostring(answer))
        
        
    def test_get_points_coordinates(self):
        ""
        points_coordinates=((0,0,0),(10,0,0),(10,10,0),(0,10,0))
        gbXML=create_gbXML()
        pl=gbXML.add_Campus().add_Building().add_Space().add_PlanarGeometry().add_PolyLoop()
        pl.create_CartesianPoints(*points_coordinates)
        
        self.assertEqual(pl.get_points_coordinates(),
                         points_coordinates)
        
        
        
if __name__=='__main__':
    
    
    unittest.main(Test_PolyLoop())
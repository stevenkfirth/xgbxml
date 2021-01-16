# -*- coding: utf-8 -*-

import unittest

from gbxml import create_gbXML
from lxml import etree


class Test_Space(unittest.TestCase):
   

    def test_create_planar_geometry(self):
        ""
        vertices=((0,0,0),(10,0,0),(10,10,0),(0,10,0))
        gbXML=create_gbXML()
        space=gbXML.add_Campus().add_Building().add_Space()
        space.create_planar_geometry(*vertices)
        #print(etree.tostring(gbXML,pretty_print=True).decode())
        
        parser=etree.XMLParser(remove_blank_text=True)
        answer=etree.fromstring("""<gbXML xmlns="http://www.gbxml.org/schema" version="6.01" temperatureUnit="C" lengthUnit="Meters" areaUnit="SquareMeters" volumeUnit="CubicMeters" useSIUnitsForResults="true">
                                  <Campus>
                                    <Building>
                                      <Space>
                                        <PlanarGeometry>
                                          <PolyLoop>
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
                                        </PlanarGeometry>
                                      </Space>
                                    </Building>
                                  </Campus>
                                </gbXML>""",
                                parser=parser)
        
        self.assertEqual(etree.tostring(gbXML),
                         etree.tostring(answer))
        
        
    def test_get_planar_geometry(self):
        ""
        vertices=((0,0,0),(10,0,0),(10,10,0),(0,10,0))
        gbXML=create_gbXML()
        space=gbXML.add_Campus().add_Building().add_Space()
        space.create_planar_geometry(*vertices)
        
        self.assertEqual(space.PlanarGeometry.get_coordinates(),
                          vertices)
        
        
        
if __name__=='__main__':
    
    
    unittest.main(Test_Space())
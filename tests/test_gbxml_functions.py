# -*- coding: utf-8 -*-
"""
Created on Mon May  9 09:39:02 2022

@author: cvskf
"""

import unittest

from lxml import etree

import xgbxml.gbxml_functions as gbxml_functions


fp=r'files\gbXMLStandard.xml'
tree = etree.parse(fp)
gbxml=tree.getroot()
ns={'gbxml':'http://www.gbxml.org/schema'}

cp=gbxml.xpath('//gbxml:CartesianPoint', namespaces=ns)[0]  # first CartesianPoint
pg=gbxml.xpath('//gbxml:PlanarGeometry', namespaces=ns)[0]  # first PlanarGeometry
rg=gbxml.xpath('//gbxml:RectangularGeometry', namespaces=ns)[0]  # first RectangularGeometry
su=gbxml.xpath('//gbxml:Surface[@id="aim12670"]', namespaces=ns)[0]  # specific surface
op=gbxml.xpath('//gbxml:Surface[@id="aim12670"]/gbxml:Opening', namespaces=ns)[0]  # specific opening

fp=r'files\GreenBuildingXML_Ver6.01.xsd'
xsd_schema = etree.parse(fp).getroot()


class Test_common(unittest.TestCase):
    ""
    
    def test_set_attribute(self):
        ""
        xml='<gbXML version="6.01" xmlns="http://www.gbxml.org/schema"></gbXML>' 
        gbxml=etree.fromstring(xml)  # root node
        gbxml_functions.set_attribute_on_gbxml_element(
            gbxml_element=gbxml,
            attribute_name='temperatureUnit',
            value='C',
            xsd_schema=xsd_schema
            )
        self.assertEqual(gbxml.attrib,
                         {'version': '6.01', 'temperatureUnit': 'C'})


class Test_CartesianPoint(unittest.TestCase):
    ""
    
    
    def test_get_Coordinate_values_from_CartesianPoint(self):
        ""
        x=gbxml_functions.get_Coordinate_values_from_CartesianPoint(cp, 
                                                                    xsd_schema)
        self.assertEqual(x,
                         (47.90424, 58.64111, 474.0))
        
       
class Test_PlanarGeometry(unittest.TestCase):
    ""
    
    def test_get_coordinate_values_from_PlanarGeometry(self):
        ""
        self.assertEqual(
            gbxml_functions.get_coordinate_values_from_PlanarGeometry(
                pg,
                xsd_schema
                ),
            ((47.90424, 58.64111, 474.0), 
             (275.3938, 58.64111, 474.0), 
             (275.3938, 165.8911, 474.0), 
             (47.90424, 165.8911, 474.0))
            )
        
    
    def test_get_shell_of_PlanarGeometry(self):
        ""
        self.assertEqual(
            gbxml_functions.get_shell_of_PlanarGeometry(
                pg,
                xsd_schema
                ),
            ((47.90424, 58.64111, 474.0), 
             (275.3938, 58.64111, 474.0), 
             (275.3938, 165.8911, 474.0), 
             (47.90424, 165.8911, 474.0),
             (47.90424, 58.64111, 474.0))
            )
    
        
        
class Test_RectangularGeometry(unittest.TestCase):
    ""
    
    def test_get_x_vector_of_RectangularGeometry(self):
        ""
        self.assertEqual(
            gbxml_functions.get_x_vector_of_RectangularGeometry(
                rg,
                xsd_schema
                ),
            (-1.8369701987210297e-16,
             -1.0,
             0.0)
            )
        
        
    def test_get_y_vector_of_RectangularGeometry(self):
        ""
        self.assertEqual(
            gbxml_functions.get_y_vector_of_RectangularGeometry(
                rg,
                xsd_schema
                ),
            (-1.1248198369963932e-32,
             -6.123233995736766e-17,
             1.0)
            )
    
    
    def test_get_shell_from_height_and_width_of_RectangularGeometry(self):
        ""
        self.assertEqual(
            gbxml_functions.get_shell_from_height_and_width_of_RectangularGeometry(
                rg,
                xsd_schema
                ),
            ((47.90423999343799, 75.5578, 474.0), 
             (47.90423999343799, 75.5578, 484.5), 
             (47.904239993438, 106.0994, 484.5), 
             (47.904239993438, 106.0994, 474.0),
             (47.90423999343799, 75.5578, 474.0))
            )
    
    
    def test_get_shell_from_polyloop_of_RectangularGeometry(self):
        ""
        self.assertEqual(
            gbxml_functions.get_shell_from_polyloop_of_RectangularGeometry(
                rg,
                xsd_schema
                ),
            ((47.90423999343799, 75.557789993438, 474.0), 
             (47.90423999343799, 75.557789993438, 484.5), 
             (47.904239993438, 106.0994, 484.5), 
             (47.904239993438, 106.0994, 474.0),
             (47.90423999343799, 75.557789993438, 474.0))
            )
   
        
        
class Test_Surface(unittest.TestCase):
    ""
    
    def test_get_holes_of_Surface(self):
       ""
       self.assertEqual(
           gbxml_functions.get_holes_of_Surface(
               su,
               xsd_schema
               ),
            [((97.35217, 67.50311, 490.0), 
              (97.35217, 70.50311, 490.0), 
              (97.35217, 70.50311, 497.0), 
              (97.35217, 67.50311, 497.0), 
              (97.35217, 67.50311, 490.0))]
            )
    
    
    def test_get_shell_of_Surface(self):
       ""
       self.assertEqual(
           gbxml_functions.get_shell_of_Surface(su,
                                                xsd_schema),
            ((97.35217, 67.50311, 490.0), 
             (97.35217, 70.50311, 490.0), 
             (97.35217, 70.50311, 497.0), 
             (97.35217, 67.50311, 497.0), 
             (97.35217, 67.50311, 490.0))
            )
    
    
    def test_get_polygon_of_Surface(self):
       ""
       self.assertEqual(
           gbxml_functions.get_polygon_of_Surface(su,
                                                  xsd_schema),
            (((97.35217, 67.50311, 490.0), 
              (97.35217, 70.50311, 490.0), 
              (97.35217, 70.50311, 497.0), 
              (97.35217, 67.50311, 497.0), 
              (97.35217, 67.50311, 490.0)), 
             [((97.35217, 67.50311, 490.0), 
               (97.35217, 70.50311, 490.0), 
               (97.35217, 70.50311, 497.0), 
               (97.35217, 67.50311, 497.0), 
               (97.35217, 67.50311, 490.0))])
            )
    
    
class Test_Opening(unittest.TestCase):
    ""
    
    def test_get_shell_of_Opening(self):
        ""
        self.assertEqual(
            gbxml_functions.get_shell_of_Opening(op,
                                                 xsd_schema),
            ((97.35217, 67.50311, 490.0), 
             (97.35217, 70.50311, 490.0), 
             (97.35217, 70.50311, 497.0), 
             (97.35217, 67.50311, 497.0),
             (97.35217, 67.50311, 490.0))
            )
    
        
        
if __name__=='__main__':
    
    unittest.main()
# -*- coding: utf-8 -*-
"""
Created on Mon May  9 09:39:02 2022

@author: cvskf
"""

import unittest

from lxml import etree
from copy import copy

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
    
    def test_add_child_to_gbxml_element(self):
        ""
        xml='<gbXML version="6.01" xmlns="http://www.gbxml.org/schema"></gbXML>' 
        gbxml=etree.fromstring(xml)  # root node
        
        # valid child name
        gbxml_functions.add_child_to_gbxml_element(
            gbxml_element=gbxml,
            child_nntag='Campus',
            xsd_schema=xsd_schema,
            )
    
        # invalid child name
        with self.assertRaises(KeyError):
            gbxml_functions.add_child_to_gbxml_element(
                gbxml_element=gbxml,
                child_nntag='xxxxxx',
                xsd_schema=xsd_schema,
                )
        
        
    
    def test_set_attribute_on_gbxml_element(self):
        ""
        xml='<gbXML version="6.01" xmlns="http://www.gbxml.org/schema"></gbXML>' 
        gbxml=etree.fromstring(xml)  # root node
        
        # correct input
        gbxml_functions.set_attribute_on_gbxml_element(
            gbxml_element=gbxml,
            attribute_name='temperatureUnit',
            value='C',
            xsd_schema=xsd_schema
            )
        self.assertEqual(gbxml.attrib,
                         {'version': '6.01', 'temperatureUnit': 'C'})
        
        # incorrect attribute name 
        with self.assertRaises(KeyError):
            gbxml_functions.set_attribute_on_gbxml_element(
                gbxml_element=gbxml,
                attribute_name='xxxxxx',
                value='C',
                xsd_schema=xsd_schema
                )
            
        
        # attribute value not in enumeration list
        with self.assertRaises(ValueError):
            gbxml_functions.set_attribute_on_gbxml_element(
                gbxml_element=gbxml,
                attribute_name='temperatureUnit',
                value='xxxxxx',
                xsd_schema=xsd_schema
                )
            
        # attribute value not same type as in schema
        with self.assertRaises(TypeError):
            gbxml_functions.set_attribute_on_gbxml_element(
                gbxml_element=gbxml,
                attribute_name='useSIUnitsForResults',
                value=6,
                xsd_schema=xsd_schema
                )
        
        
    
    def test_set_value_of_gbxml_element(self):
        ""
        xml='''<gbXML version="6.01" xmlns="http://www.gbxml.org/schema">
        <Campus><Name/></Campus></gbXML>'''
        gbxml=etree.fromstring(xml)  # root node
        campus=gbxml[0]
        name=campus[0]
        
        # correct value type
        gbxml_functions.set_value_of_gbxml_element(
            gbxml_element=name,
            value='campus1',
            xsd_schema=xsd_schema
            )
        
        # incorrect value type
        with self.assertRaises(TypeError):
            gbxml_functions.set_value_of_gbxml_element(
                gbxml_element=name,
                value=1234,
                xsd_schema=xsd_schema
                )
        
        
        


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
    
    def test_copy_Opening_to_Surface(self):
        ""
        #print(etree.tostring(copy(op)).decode())
        x=gbxml_functions.copy_Opening_to_Surface(
            gbxml_opening=copy(op),
            gbxml_surface=copy(su), 
            xsd_schema=xsd_schema,
            tolerance=0.01)
        
        
    def test_get_new_coordinate_system_of_Surface(self):
        ""
        
        result=gbxml_functions.get_new_coordinate_system_of_Surface(
            su,
            xsd_schema
            )
        self.assertEqual(
            result,
            ((97.35217, 67.50311, 490.0), 
             (0.0, 1.0, 0.0), 
             (-0.0, -0.0, 1.0), 
             (1.0, 0.0, 0.0))
            )
    
    
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
    
    def xtest_create_rectangular_geometry_from_PlanarGeometry_for_Opening(self):
        ""
        
        
        
        
        gbxml_functions.create_rectangular_geometry_from_PlanarGeometry_for_Opening(
            op,
            xsd_schema
            )
    
    
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
    
    
    def test_set_shell_of_opening(self):
        ""
        op2=copy(op)
        x=gbxml_functions.set_shell_of_Opening(
            op2,
            ((97.35217, 67.50311, 491.0), 
             (97.35217, 70.50311, 491.0), 
             (97.35217, 70.50311, 496.0), 
             (97.35217, 67.50311, 496.0),
             (97.35217, 67.50311, 491.0)),
            xsd_schema
            )
        self.assertEqual(
            gbxml_functions.get_shell_of_Opening(op2,
                                                 xsd_schema),
            ((97.35217, 67.50311, 491.0), 
             (97.35217, 70.50311, 491.0), 
             (97.35217, 70.50311, 496.0), 
             (97.35217, 67.50311, 496.0),
             (97.35217, 67.50311, 491.0))
            )
    
        
        
if __name__=='__main__':
    
    unittest.main()
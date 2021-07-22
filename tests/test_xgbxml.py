# -*- coding: utf-8 -*-

import unittest

from xgbxml import get_parser, create_gbXML
from lxml import etree
from crossproduct import Point, Vector, Polyline, Polygon

fp=r'files\gbXMLStandard.xml'
parser=get_parser(version='0.37')
tree = etree.parse(fp,parser)

class Test_get_parser(unittest.TestCase):
    ""
   
    def test_get_parser(self):
        ""
        parser=get_parser(version='0.37')
        self.assertIsInstance(parser,etree.XMLParser)
        
        
    def test_parse(self):
        ""
        self.assertIsInstance(tree,etree._ElementTree)
        
        
        
class Test_create_gbXML(unittest.TestCase):
    ""
        
    def test_create_gbXML(self):
        ""
        gbXML=create_gbXML()
        self.assertEqual(gbXML.__class__.__name__,
                         'gbXML')



class Test_gbXML(unittest.TestCase):
    ""
    
    def test_add_campus(self):
        ""
        gbXML=create_gbXML()
        campus=gbXML.add_Campus()
        self.assertEqual(campus.__class__.__name__,
                         'Campus')
        
        
        
class Test_Campus(unittest.TestCase):
    ""

    def test_get_Space(self):
        ""
        gbXML=tree.getroot()
        campus=gbXML.Campus
        space=campus.get_Space('aim0119')
        self.assertEqual(space.nntag,
                         'Space')
        self.assertEqual(space.id,
                         'aim0119')
        
        
    def test_plot_surfaces(self):
        ""
        return
        #fp=r'files\ExerciseFacility (Older).xml'
        fp=r'files\gbXMLStandardv Retail Big Box.xml'
        parser=get_parser(version='0.37')
        tree = etree.parse(fp,parser)
        gbXML=tree.getroot()
        ca=gbXML.Campus
        ca.plot_surfaces(surfaceType='Roof')
        
        

class Test_CartesianPoint(unittest.TestCase):
    ""


    def test_get_coordinates(self):
        ""
        gbXML=tree.getroot()
        cp=gbXML.Campus.Surface.PlanarGeometry.PolyLoop.CartesianPoint
        self.assertEqual(cp.get_coordinates(),
                         (47.90424, 75.55779, 474.0))
        

    def test_get_Point(self):
        ""
        gbXML=tree.getroot()
        cp=gbXML.Campus.Surface.PlanarGeometry.PolyLoop.CartesianPoint
        self.assertEqual(cp.get_Point(),
                         Point(47.90424, 75.55779, 474.0))
        
        
    def test_plot(self):
        ""
        return
        gbXML=tree.getroot()
        cp=gbXML.Campus.Surface.PlanarGeometry.PolyLoop.CartesianPoint
        ax=cp.plot()
        print(type(ax))
        
        

class Test_ClosedShell(unittest.TestCase):
    ""
    
    
    
class Test_Location(unittest.TestCase):
    ""



class Test_PlanarGeometry(unittest.TestCase):
    ""
    
    def test_get_coordinates(self):
        ""
        gbXML=tree.getroot()
        pg=gbXML.Campus.Surface.PlanarGeometry
        self.assertEqual(pg.get_coordinates(),
                         ((47.90424, 75.55779, 474.0), 
                          (47.90424, 75.55779, 484.5), 
                          (47.90424, 106.0994, 484.5), 
                          (47.90424, 106.0994, 474.0)))
    
    
    def test_get_Polygon(self):
        ""
        gbXML=tree.getroot()
        pg=gbXML.Campus.Surface.PlanarGeometry
        self.assertEqual(pg.get_Polygon(),
                         Polygon(Point(47.90424,75.55779,474.0),
                                       Point(47.90424,75.55779,484.5),
                                       Point(47.90424,106.0994,484.5),
                                       Point(47.90424,106.0994,474.0)))
        
        
    def _test_plot(self):
        ""
        #return
        gbXML=tree.getroot()
        pg=gbXML.Campus.Surface.PlanarGeometry
        ax=pg.plot()
        print(type(ax))
    
    
    def _test_render(self):
        gbXML=tree.getroot()
        pg=gbXML.Campus.Surface.PlanarGeometry
        scene=pg.render()
        print(scene)




class Test_RectangularGeometry(unittest.TestCase):
    ""
    
    def test__get_x_vector(self):
        ""
        gbXML=tree.getroot()
        rg=gbXML.Campus.Surface.RectangularGeometry
        self.assertEqual(rg._get_x_vector(),
                         Vector(-1.8369701987210297e-16,
                                -1.0,
                                0.0))
        
        
    def test__get_y_vector(self):
        ""
        gbXML=tree.getroot()
        rg=gbXML.Campus.Surface.RectangularGeometry
        self.assertEqual(rg._get_y_vector(),
                         Vector(-1.1248198369963932e-32,
                                -6.123233995736766e-17,
                                1.0))
    
    
    def test_get_coordinates_from_height_and_width(self):
        ""
        gbXML=tree.getroot()
        rg=gbXML.Campus.Surface.RectangularGeometry
        self.assertEqual(rg.get_coordinates_from_height_and_width(),
                         ((47.90423999343799, 75.5578, 474.0), 
                          (47.90423999343799, 75.5578, 484.5), 
                          (47.904239993438, 106.0994, 484.5), 
                          (47.904239993438, 106.0994, 474.0)))
    
    
    def test_get_coordinates_from_polyloop(self):
        ""
        gbXML=tree.getroot()
        rg=gbXML.Campus.Surface.RectangularGeometry
        self.assertEqual(rg.get_coordinates_from_polyloop(),
                         ((47.90423999343799, 75.557789993438, 474.0), 
                          (47.90423999343799, 75.557789993438, 484.5), 
                          (47.904239993438, 106.0994, 484.5), 
                          (47.904239993438, 106.0994, 474.0)))
        
        
    def test_get_SimplePolygon_from_height_and_width(self):
        ""
        gbXML=tree.getroot()
        rg=gbXML.Campus.Surface.RectangularGeometry
        self.assertEqual(rg.get_Polygon_from_height_and_width(),
                         Polygon(Point(47.90423999343799,75.5578,474.0),
                                       Point(47.90423999343799,75.5578,484.5),
                                       Point(47.904239993438,106.0994,484.5),
                                       Point(47.904239993438,106.0994,474.0)))



class Test_PolyLoop(unittest.TestCase):
    ""
    
    def test_get_coordinates(self):
        ""
        gbXML=tree.getroot()
        pl=gbXML.Campus.Surface.PlanarGeometry.PolyLoop
        self.assertEqual(pl.get_coordinates(),
                         ((47.90424, 75.55779, 474.0), 
                          (47.90424, 75.55779, 484.5), 
                          (47.90424, 106.0994, 484.5), 
                          (47.90424, 106.0994, 474.0)))
    
    
    def test_get_Polyline(self):
        ""
        gbXML=tree.getroot()
        pl=gbXML.Campus.Surface.PlanarGeometry.PolyLoop
        self.assertEqual(pl.get_Polyline(),
                         Polyline(Point(47.90424,75.55779,474.0),
                                  Point(47.90424,75.55779,484.5),
                                  Point(47.90424,106.0994,484.5),
                                  Point(47.90424,106.0994,474.0)))
        
        
    def test_plot(self):
        ""
        return
        gbXML=tree.getroot()
        pl=gbXML.Campus.Surface.PlanarGeometry.PolyLoop
        ax=pl.plot()
        print(type(ax))
    
    
class Test_Space(unittest.TestCase):
    ""
    
    
    
class Test_Surface(unittest.TestCase):
    ""
    
    def test_get_coordinates(self):
        ""
        gbXML=tree.getroot()
        su=gbXML.Campus.Surface
        self.assertEqual(su.get_coordinates(),
                         (((47.90424, 75.55779, 474.0), 
                          (47.90424, 75.55779, 484.5), 
                          (47.90424, 106.0994, 484.5), 
                          (47.90424, 106.0994, 474.0)),))
    
    
    def test_get_SimplePolygon(self):
        ""
        gbXML=tree.getroot()
        su=gbXML.Campus.Surface
        self.assertEqual(su.get_Polygon(),
                         Polygon(Point(47.90424,75.55779,474.0),
                                       Point(47.90424,75.55779,484.5),
                                       Point(47.90424,106.0994,484.5),
                                       Point(47.90424,106.0994,474.0)))
        
        
    def test_plot(self):
        ""
        gbXML=tree.getroot()
        
        return
        su=gbXML.Campus.get_child('Surface',child_id='aim89302')
        su.PlanarGeometry.plot()
        su.Opening.plot()
        print(len(su.get_coordinates()))
        
        # surface with opening (here opening is the whole od the surface)
        return
        su=gbXML.Campus.get_child('Surface',child_id='aim12670')
        su.plot()
        
        # surface with no opening
        return
        su=gbXML.Campus.Surface
        ax=su.plot()
        print(type(ax))
        
        
    


class Test_Opening(unittest.TestCase):
    ""
    
    def test_get_coordinates(self):
        ""
        gbXML=tree.getroot()
        op=gbXML.Campus.get_child('Surface',child_id='aim12670').Opening
        #op.display()
        self.assertEqual(op.get_coordinates(),
                         ((97.35217, 67.50311, 490.0), 
                          (97.35217, 70.50311, 490.0), 
                          (97.35217, 70.50311, 497.0), 
                          (97.35217, 67.50311, 497.0)))
        
        
    def test_get_Polygon(self):
        ""
        gbXML=tree.getroot()
        op=gbXML.Campus.get_child('Surface',child_id='aim12670').Opening
        self.assertEqual(op.get_Polygon(),
                         Polygon(Point(97.35217,67.50311,490.0),
                                       Point(97.35217,70.50311,490.0),
                                       Point(97.35217,70.50311,497.0),
                                       Point(97.35217,67.50311,497.0)))
        
    def test_plot(self):
        ""
        return
        gbXML=tree.getroot()
        op=gbXML.Campus.get_child('Surface',child_id='aim12670').Opening
        op.plot()








    
if __name__=='__main__':
    
    unittest.main()
    
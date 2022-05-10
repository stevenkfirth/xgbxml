# -*- coding: utf-8 -*-


import unittest

from xgbxml import get_parser, create_gbXML
from xgbxml.xgbxml import gbCollection
from lxml import etree


fp=r'files\gbXMLStandard.xml'
parser=get_parser(version='0.37')
tree = etree.parse(fp,parser)
        

        
class Test_gbElement(unittest.TestCase):
    ""
    
    def test_get_children(self):
        ""
        gbXML=tree.getroot()
        self.assertIsInstance(gbXML.Campuss,
                              gbCollection)
    
    
class Test_gbCollection(unittest.TestCase):
    ""
    
    def test___getattr__(self):
        ""
        gbXML=tree.getroot()
        
        cs=gbXML.Campuss
        
        
        return
        print(cs.id)
        
        
        print(gbXML.Campuss.Surfaces[:10])
        
        
        print(gbXML.Campus.Surfaces.Openings)
        
        
        #print(gbXML.Campus.Surfaces.PlanarGeometrys[:10].get_Polygon)
        
        #print(gbXML.Campus.Surfaces.PlanarGeometrys[:10].get_Polygon())
    
    
    def test___get_item__(self):
        ""
        gbXML=tree.getroot()
        
        # test slice
        self.assertIsInstance(gbXML.Campuss[:],
                              gbCollection)
    
    
    

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

    # def test_get_Space(self):
    #     ""
    #     gbXML=tree.getroot()
    #     campus=gbXML.Campus
    #     space=campus.get_Space('aim0119')
    #     self.assertEqual(space.nntag,
    #                      'Space')
    #     self.assertEqual(space.id,
    #                      'aim0119')
        
        
    def test_render(self):
        ""
        return
        gbXML=tree.getroot()
        campus=gbXML.Campus
        campus.render()
        
        

class Test_CartesianPoint(unittest.TestCase):
    ""


    def test_get_coordinates(self):
        ""
        gbXML=tree.getroot()
        cp=gbXML.Campus.Surface.PlanarGeometry.PolyLoop.CartesianPoint
        self.assertEqual(
            cp.get_coordinates(),
            (47.90424, 75.55779, 474.0)
            )
        
    

class Test_PlanarGeometry(unittest.TestCase):
    ""    
    
    def _test_render(self):
        ""
        return
        gbXML=tree.getroot()
        pg=gbXML.Campus.Surface.PlanarGeometry
        scene=pg.render()
        print(scene)




class Test_RectangularGeometry(unittest.TestCase):
    ""
    
    
        
    def test_render(self):
        ""
        return
        gbXML=tree.getroot()
        rg=gbXML.Campus.Surface.RectangularGeometry
        ax=rg.render()
        
        
        
    # def xtest_get_SimplePolygon_from_height_and_width(self):
    #     ""
    #     gbXML=tree.getroot()
    #     rg=gbXML.Campus.Surface.RectangularGeometry
    #     self.assertEqual(rg.get_Polygon_from_height_and_width(),
    #                      Polygon(Point(47.90423999343799,75.5578,474.0),
    #                                    Point(47.90423999343799,75.5578,484.5),
    #                                    Point(47.904239993438,106.0994,484.5),
    #                                    Point(47.904239993438,106.0994,474.0)))



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
        
        
    def test_get_shell(self):
        ""
        gbXML=tree.getroot()
        pl=gbXML.Campus.Surface.PlanarGeometry.PolyLoop
        #print(pl.get_shell())
        self.assertEqual(pl.get_shell(),
                         ((47.90424, 75.55779, 474.0), 
                          (47.90424, 75.55779, 484.5), 
                          (47.90424, 106.0994, 484.5), 
                          (47.90424, 106.0994, 474.0),
                          (47.90424, 75.55779, 474.0)))
    
    
    
        
        
    def test_render(self):
        ""
        return
        gbXML=tree.getroot()
        pl=gbXML.Campus.Surface.PlanarGeometry.PolyLoop
        ax=pl.render()
        
    
    
class Test_Space(unittest.TestCase):
    ""
    
    
    
class Test_Surface(unittest.TestCase):
    ""
    
    
    
    
    
    def test_render(self):
        ""
        return
        gbXML=tree.getroot()
       
        # opening is whole surface
        su=gbXML.Campus.get_child('Surface',child_id='aim12670')
        su.render()
    
        # no opening in surface
        su=gbXML.Campus.Surface
        su.render()
        
        
    
    


class Test_Opening(unittest.TestCase):
    ""
    
    
        
        
    
        
        
    def test_render(self):
        ""
        return
        gbXML=tree.getroot()
        op=gbXML.Campus.get_child('Surface',child_id='aim12670').Opening
        op.render()




class Test_Material(unittest.TestCase):
    ""
    
    def test_add_R_value(self):
        ""
        gbXML=create_gbXML()
        m=gbXML.add_Material()
        #print(m)
        z=gbXML.add_Zone()
        #print(z)
        #rv=m.add_R_value(unit='W')   # TO FIX
        #print(rv)
        
        






    
if __name__=='__main__':
    ""
    
    unittest.main()
    
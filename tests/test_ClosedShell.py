# -*- coding: utf-8 -*-

import unittest

from gbxml import create_gbXML
from lxml import etree


class Test_ClosedShell(unittest.TestCase):
   

    def test_create_PolyLoops(self):
        ""
        points_coordinates=((0,0,0),(10,0,0),(10,10,0),(0,10,0))
        polyloops_points_coordinates=(points_coordinates,points_coordinates)
        gbXML=create_gbXML()
        cs=gbXML.add_Campus().add_Building().add_Space().add_ShellGeometry().add_ClosedShell()
        polyloops=cs.create_PolyLoops(*polyloops_points_coordinates)
        #print(etree.tostring(cs,pretty_print=True).decode())
        self.assertEqual(len(polyloops),
                         2)
        
        
    def test_get_polyloops_points_coordinates(self):
        ""
        points_coordinates=((0,0,0),(10,0,0),(10,10,0),(0,10,0))
        polyloops_points_coordinates=(points_coordinates,points_coordinates)
        gbXML=create_gbXML()
        cs=gbXML.add_Campus().add_Building().add_Space().add_ShellGeometry().add_ClosedShell()
        cs.create_PolyLoops(*polyloops_points_coordinates)
        
        self.assertEqual(cs.get_polyloops_points_coordinates(),
                         polyloops_points_coordinates)
        
        
        
if __name__=='__main__':
    
    
    unittest.main(Test_ClosedShell())
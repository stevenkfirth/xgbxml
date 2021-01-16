# -*- coding: utf-8 -*-

class PlanarGeometry():
    ""
    
    def create_poly_loop(self,*vertices):
        ""
        
        self.add_PolyLoop().create_cartesian_points(*vertices)
        
        
    def get_coordinates(self):
        ""
        return self.PolyLoop.get_coordinates()
# -*- coding: utf-8 -*-

class PolyLoop():
    ""
    
    def create_cartesian_points(self,*vertices):
        ""
        #print(vertices)
        for vertex in vertices:
            self.add_CartesianPoint().create_coordinates(*vertex)
            
            
    def get_coordinates(self):
        ""
        return tuple([cp.get_coordinates() for cp in self.CartesianPoints])
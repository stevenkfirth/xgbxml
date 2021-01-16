# -*- coding: utf-8 -*-

class CartesianPoint():
    ""
    
    def create_coordinates(self,*coordinates):
        """
        
        """
        #print(coordinates)
        for coordinate in coordinates:
            self.add_Coordinate().value=coordinate
            
    def get_coordinates(self):
        ""
        return tuple([co.value for co in self.Coordinates])
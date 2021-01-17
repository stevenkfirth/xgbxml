# -*- coding: utf-8 -*-

class CartesianPoint():
    ""
    
    def create_Coordinates(self,*coordinates):
        """Creates Coordinate child elements and sets their value.
        
        :param coordinatess: The values of the x,y,(z) coordinates as an argument list.
        :type coordinates: int, float
        
        :returns: The newly creeated Coordinate elements.
        :rtype: list(Coordinate)
        
        """
        #print(coordinates)
        for coordinate in coordinates:
            self.add_Coordinate().value=coordinate
        return self.Coordinates
            
            
    def get_coordinates(self):
        """Returns the values of the Coordinate child elements.
        
        :rtype: tuple(float)
        
        """
        return tuple([co.value for co in self.Coordinates])
# -*- coding: utf-8 -*-

class PolyLoop():
    ""
    
    def create_CartesianPoints(self,*points_coordinates):
        """Creates CartesianPoint child elements with Coordinate subelements.
        
        :param points_coordinates: An argument list of tuple where each tuple is 
            the (x,y,(z)) coordinates of a CartesianPoint.
        :type points_coordinates: tuple
        
        :returns: The newly creeated CartesianPoint elements.
        :rtype: list(CartesianPoints)
        
        """
        for point_coordinates in points_coordinates:
            self.add_CartesianPoint().create_Coordinates(*point_coordinates)
        return self.CartesianPoints
            
            
    def get_points_coordinates(self):
        """Returns the coordinates of the CartesianPoint child elements.
        
        :returns: Point_coordinates where each point_coordinate is a tuple of 
            the (x,y,(z)) coordinates of a CartesianPoint.
        :rtype: tuple(tuple(float))
        
        """
        return tuple([cp.get_coordinates() for cp in self.CartesianPoints])
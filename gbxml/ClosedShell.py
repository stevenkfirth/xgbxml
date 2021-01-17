# -*- coding: utf-8 -*-

class ClosedShell():
    ""
    
    def create_PolyLoops(self,*polyloops_points_coordinates):
        """Creates PolyLoop child elements with CartesianPoint ans Coordinate subelements.
        
        :param polyloop_points_coordinates: An argument list of tuple where each tuple is 
            the vertex_values of a PolyLoop.
        :type polyloop_points_coordinates: tuple
        
        :returns: The newly creeated PolyLoop elements.
        :rtype: list(PolyLoop)
        
        """
        for polyloop_points_coordinates in polyloops_points_coordinates:
            self.add_PolyLoop().create_CartesianPoints(*polyloop_points_coordinates)
        return self.PolyLoops
        
            
    def get_polyloops_points_coordinates(self):
        """Returns the polyloop coordinate values of the PolyLoop child elements.
        
        :returns: Polygon values where each value is a tuple of 
            the vertex_values of a PolyLoop.
        :rtype: tuple(tuple(tuple(float)))
        
        """
        return tuple([pl.get_points_coordinates() for pl in self.PolyLoops])


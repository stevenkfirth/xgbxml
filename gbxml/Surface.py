# -*- coding: utf-8 -*-

class Surface():
    ""
    
    
    def get_Campus(self):
        """Returns the campus element that this surface belongs to.
        
        :rtype: Campus
        
        """
        return self.getparent()
    
    
    def get_Spaces(self):
        """Returns the space elements adjacent to the surface.
        
        """
        c=self.get_Campus()
        return [c.get_Space(AdjacentSpaceId.spaceIdRef) for AdjacentSpaceId in self.AdjacentSpaceIds]
        
        
        
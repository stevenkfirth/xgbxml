# -*- coding: utf-8 -*-

class Space():
    """
    """
    
    def create_planar_geometry(self,*vertices):
        """
    
        """
        
        self.add_PlanarGeometry().create_poly_loop(*vertices)
        
        return
        
        # need to delete and existing PlanarGeometry
        
        pg=self.add_PlanarGeometry()
        pl=pg.add_PolyLoop()
        for vertex in vertices:
            cp=pl.add_CartesianPoint()
            for coordinate in vertex:
                cp.add_Coordinate().value=coordinate
            
    
    def create_shell_geometry(self):
        """
        """
        
    
    
    
    
        
    
        
        
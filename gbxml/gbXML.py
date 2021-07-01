# -*- coding: utf-8 -*-

from crossproduct import Point, Vector, SimplePolygon
import math

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class gbXML():
    ""
    
class Campus():
    ""
    
    def get_Space(self,id):
        """Returns a Space element belonging to the Campus.
        
        :raises KeyError: If the space does not exist.
        
        :rtype: Space
        
        """
        try:
            return self.xpath(r'./gbxml:Building/gbxml:Space[@id="%s"]' % (id),
                              namespaces=self._ns)[0]
        except IndexError:
            raise KeyError('Element with id="%s" does not exist in the xml tree.' % id)
    
    
    def plot_surfaces(self,
                      ax=None,
                      **kwargs):
        """Plots the surface.
        
        :rtype: matplotlib.axes._subplots.Axes3DSubplot
        
        """
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
        
        for su in self.Surfaces:
            #print(su)
            su.plot(ax,
                    set_axis_limits=False,
                    alpha=0.5,
                    **kwargs)
            su.PlanarGeometry.plot(ax,
                                   set_axis_limits=False,
                                   linewidth=0.5,
                                   color='white')
            
            #break
        
        x_values,y_values,z_values=[],[],[]
        for su in self.Surfaces:
            cs=su.get_coordinates()
            x_values.extend([c[0] for c in cs])
            y_values.extend([c[1] for c in cs])
            z_values.extend([c[2] for c in cs])
        
        
        ax.set_xlim(min(x_values),max(x_values))
        ax.set_ylim(min(y_values),max(y_values))
        ax.set_zlim(min(z_values),max(z_values))
        
        return ax
        
    
    
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
    
    
    def get_Point(self):
        """Returns a Point for the cartesian point.
        
        :rtype: crossproduct.Point
        
        """
        return Point(*self.get_coordinates())
    
    
    def plot(self,ax=None,**kwargs):
        """Plots the cartesian point
        
        :rtype: matplotlib.axes._subplots.Axes3DSubplot
        
        """
        return self.get_Point().plot(ax=ax,**kwargs)
    
    
    
class ClosedShell():
    ""
    
    def create_PolyLoops(self,*polyloops_points_coordinates):
        """Creates PolyLoop child elements with CartesianPoint and Coordinate subelements.
        
        :param polyloop_points_coordinates: An argument list of tuple where each tuple is 
            the vertex_values of a PolyLoop.
        :type polyloop_points_coordinates: tuple
        
        :returns: The newly creeated PolyLoop elements.
        :rtype: list(PolyLoop)
        
        """
        for polyloop_points_coordinates in polyloops_points_coordinates:
            self.add_PolyLoop().create_CartesianPoints(*polyloop_points_coordinates)
        return self.PolyLoops
        
            
    def get_coordinates(self):
        """Returns the polyloop coordinate values of the PolyLoop child elements.
        
        :returns: Polygon values where each value is a tuple of 
            the vertex_values of a PolyLoop.
        :rtype: tuple(tuple(tuple(float)))
        
        """
        return tuple([pl.get_coordinates() for pl in self.PolyLoops])



class Location():
    ""
    
    
    
class PlanarGeometry():
    ""
    
    def get_coordinates(self):
        """Returns the coordinates of the polyloop child element.
        
        :returns: Point_coordinates where each point_coordinate is a tuple of 
            the (x,y,(z)) coordinates of a CartesianPoint.
        :rtype: tuple(tuple(float))
        
        """
        return self.PolyLoop.get_coordinates()
    
    
    def get_SimplePolygon(self):
        """Returns a SimplePolygon of the polyloop child element.
        
        :rtype: crossproduct.SimplePolygon
        
        """
        
        return self.PolyLoop.get_SimplePolygon()
    

    def plot(self,
             ax=None,
             set_axis_limits=True,
             **kwargs):
        """Plots the planar geometry.
        
        :rtype: matplotlib.axes._subplots.Axes3DSubplot
        
        """
        sp=self.get_SimplePolygon()
        
        if ax is None:
            if sp.nD==2:
                fig, ax = plt.subplots()
            else:
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
        
        if not 'color' in kwargs:
            kwargs['color']='tab:blue'
        if not 'alpha' in kwargs:
             kwargs['alpha']=0.25
        
        ax.add_collection3d(Poly3DCollection([sp.to_tuple()],
                                              **kwargs))
        
        if set_axis_limits:
        
            x_values=[c[0] for c in sp]
            y_values=[c[1] for c in sp]
            z_values=[c[2] for c in sp]
            
            ax.set_xlim(min(x_values),max(x_values))
            ax.set_ylim(min(y_values),max(y_values))
            ax.set_zlim(min(z_values),max(z_values))
        
        return ax
    
    
    
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
            
            
    def get_coordinates(self):
        """Returns the coordinates of the CartesianPoint child elements.
        
        :returns: Point_coordinates where each point_coordinate is a tuple of 
            the (x,y,(z)) coordinates of a CartesianPoint.
        :rtype: tuple(tuple(float))
        
        """
        return tuple([cp.get_coordinates() for cp in self.CartesianPoints])
    
    
    def get_SimplePolygon(self):
        """Returns a SimplePolygon of the polyloop.
        
        :rtype: crossproduct.SimplePolygon
        
        """
        
        return SimplePolygon(*[cp.get_Point() for cp in self.CartesianPoints])
    

    def plot(self,ax=None,**kwargs):
        """Plots the polyloop.
        
        :rtype: matplotlib.axes._subplots.Axes3DSubplot
        
        """
        return self.get_SimplePolygon().plot(ax=ax,**kwargs)
    

class RectangularGeometry():
    """
    """
    
    ### needs updating if the RectangularGeometry is for an Opening
    
    def _get_x_vector(self):
        "Returns the 3D vector for the x direction in the rectangular coordinate system"
        azimuth=self.Azimuth.value
        sin_azimuth=math.sin(math.radians(azimuth))
        cos_azimuth=math.cos(math.radians(azimuth))
        return Vector(cos_azimuth,
                      sin_azimuth,
                      0).normalise
    
        
    def _get_y_vector(self):
        "Returns the 3D vector for the y direction in the rectangular coordinate system"
        x_vector=self._get_x_vector()
        tilt=self.Tilt.value
        sin_tilt=math.sin(math.radians(tilt))
        cos_tilt=math.cos(math.radians(tilt))
        return Vector(x_vector[0]*cos_tilt,
                      x_vector[1]*cos_tilt,
                      sin_tilt).normalise
    
    
    def get_coordinates_from_height_and_width(self):
        """Returns the coordintes from the rectangular data using the height and width.
        
        :rtype: tuple(tuple(float))

        """
        if self.getparent().nntag=='Surface':
            
            x_vector=self._get_x_vector()
            y_vector=self._get_y_vector()
            start_point=self.CartesianPoint.get_Point()
            height=self.Height.value
            width=self.Width.value        
            
            return ((start_point+x_vector*width).to_tuple(),
                    (start_point+x_vector*width+y_vector*height).to_tuple(),
                    (start_point+y_vector*height).to_tuple(),
                    (start_point).to_tuple())
        
        else:
            raise Exception('To do')  # i.e. for openings
    
    
    def get_coordinates_from_polyloop(self):
        """Returns the coordintes from the rectangular data using the polyloop.
        
        :rtype: tuple(tuple(float))

        """
        if self.getparent().nntag=='Surface':
            
            x_vector=self._get_x_vector()
            y_vector=self._get_y_vector()
            start_point=self.CartesianPoint.get_Point()
            c2d=self.PolyLoop.get_coordinates()     
            
            return tuple((start_point+x_vector*c[0]+y_vector*c[1]).to_tuple() for c in c2d)
    
        else:
            raise Exception('To do')  # i.e. for openings
            
            
    
    def get_SimplePolygon_from_height_and_width(self):
        """Returns a SimplePolygon derived from the rectangular data using the height and width.
        
        :rtype: crossproduct.SimplePolygon

        """
        return SimplePolygon(*[Point(*c) for c in self.get_coordinates_from_height_and_width()])
    
    
    def get_SimplePolygon_from_polyloop(self):
        """Returns a SimplePolygon derived from the rectangular data using the polyloop.
        
        The child polyloop data is not used.
        
        :rtype: crossproduct.SimplePolygon

        """
        return SimplePolygon(*[Point(*c) for c in self.get_coordinates_from_polyloop()])



class Space():
    """
    """
    
    
    
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
        
    
    def get_coordinates(self):
        """Returns the coordinates of the outer polyloop of the surface.
        
        The following sources are tried in order:
            - PlanarGeometry
            - RectangularGeometry/PolyLoop
            - RectangularGeoemetry... from height and width
            
        :rtype: tuple(tuple(float))
            
        """
        try:
            return self.PlanarGeometry.get_coordinates()
        except KeyError:
            try:
                self.RectangularGeoemetry.get_coordinates_from_polyloop()
            except KeyError:
                self.RectangularGeometry.get_coordinates_from_height_and_width()
                
                
    def get_SimplePolygon(self):
        """Returns a SimplePolygon of the outer polyloop of the surface.
        
        The following sources are tried in order:
            - PlanarGeometry
            - RectangularGeometry/PolyLoop
            - RectangularGeoemetry... from height and width
            
        :rtype: crossproduct.SimplePolygon
            
        """
        return SimplePolygon(*[Point(*c) for c in self.get_coordinates()])
    
    
    def plot(self,
             ax=None,
             wall_color='tab:blue',
             roof_color='tab:red',
             shade_color='tab:olive',
             set_axis_limits=True,
             **kwargs):
        """Plots the surface.
        
        :rtype: matplotlib.axes._subplots.Axes3DSubplot
        
        """
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
        
        if not 'color' in kwargs:
            if self.surfaceType=='Shade':
                kwargs['color']=shade_color
            elif self.surfaceType=='Roof':
                kwargs['color']=roof_color
            else:
                kwargs['color']=wall_color
        if not 'alpha' in kwargs:
             kwargs['alpha']=0.25
        
        
        #if self.Openings:
            #print(self.id)
            #print(self.Openings)
            #raise Exception
        
        
        sp=self.get_SimplePolygon()
        print(sp)
        opening_polygons=[op.get_SimplePolygon() for op in self.Openings]
        print(opening_polygons)
        
        
        if opening_polygons:
            print('test')
            print(self)
            dpgs=sp.difference_simple_polygons(opening_polygons)
            print('done')
        else:
            dpgs=[sp]
            
        ax.add_collection3d(Poly3DCollection([dpg.to_tuple() for dpg in dpgs],
                                              #linewidths=0,
                                              **kwargs))
        
        # for pg in opening_polygons:
        #     pg.plot(ax)
        
        
        
        # ax.add_collection3d(Poly3DCollection([sp.to_tuple()],
        #                                      **kwargs))
        
        if set_axis_limits:
        
            x_values=[c[0] for c in sp]
            y_values=[c[1] for c in sp]
            z_values=[c[2] for c in sp]
            
            ax.set_xlim(min(x_values),max(x_values))
            ax.set_ylim(min(y_values),max(y_values))
            ax.set_zlim(min(z_values),max(z_values))
        
        return ax
    
    
    
class Opening():
    ""
    
    def get_coordinates(self):
        """Returns the coordinates of the outer polyloop of the opening.
        
        The following sources are tried in order:
            - PlanarGeometry
            - RectangularGeometry/PolyLoop
            - RectangularGeoemetry... from height and width
            
        :rtype: tuple(tuple(float))
            
        """
        try:
            return self.PlanarGeometry.get_coordinates()
        except KeyError:
            try:
                self.RectangularGeoemetry.get_coordinates_from_polyloop()
            except KeyError:
                self.RectangularGeometry.get_coordinates_from_height_and_width()
                
                
    def get_SimplePolygon(self):
        """Returns a SimplePolygon of the outer polyloop of the opening.
        
        The following sources are tried in order:
            - PlanarGeometry
            - RectangularGeometry/PolyLoop
            - RectangularGeoemetry... from height and width
            
        :rtype: crossproduct.SimplePolygon
            
        """
        return SimplePolygon(*[Point(*c) for c in self.get_coordinates()])
        
    
    def plot(self,ax=None,**kwargs):
        """Plots the opening.
        
        :rtype: matplotlib.axes._subplots.Axes3DSubplot
        
        """
        return self.get_SimplePolygon().plot(ax=ax,**kwargs)
    
    
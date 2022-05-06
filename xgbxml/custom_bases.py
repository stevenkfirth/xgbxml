# -*- coding: utf-8 -*-

#from crossproduct import Point, Vector, Polyline, Polylines, Polygon, Polygons
import math

#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
#from mpl_toolkits.mplot3d.art3d import Line3DCollection,Poly3DCollection

from . import render_functions
from .geometry_functions import vector_normalize_3d, vector_multiplication_3d, vector_addition_3d

#import vpython

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
    
    
    def get_Spaces(self):
        """Returns all Space elements belonging to the Campus.
        
        :rtype: list
        
        """
        return self.xpath(r'./gbxml:Building/gbxml:Space',
                          namespaces=self._ns)
    
    
    def get_Openings(self):
        """Returns all Opening elements belonging to the Campus.
        
        :rtype: list
        
        """
        return self.xpath(r'./gbxml:Surface/gbxml:Opening',
                          namespaces=self._ns)
        
    def render(self,
               ax=None, 
               set_lims=True, 
               outline_kwargs=None,
               surface_kwargs=None):
        """
        """
        #print(self)
        for su in self.Surfaces:
            try:
                ax=su.render(ax=ax)
            except Exception as err:
                print(su)
                print(type(err))
                
        return ax
    
    # def get_Surface_polygons(self):
    #     """
    #     :rtype: crossproduct.Polygons
    #     """
    #     return Polygons(*[su.get_Polygon() for su in self.Surfaces])
    
    # def get_Surface_PlanarGeometry_polygons(self):
    #     """
    #     :rtype: crossproduct.Polygons
    #     """
    #     return Polygons(*[su.PlanarGeometry.get_Polygon() for su in self.Surfaces])
    
    # def get_Opening_polygons(self):
    #     """
    #     :rtype: crossproduct.Polygons
    #     """
    #     result=[]
    #     for op in self.get_Openings():
    #         result.append(op.get_Polygon())
    #     return Polygons(*result)
    
    
    
    
    
    
    # def plot_surfaces(self,
    #                   ax=None,
    #                   surfaceType=None,
    #                   **kwargs):
    #     """Plots the surface.
        
    #     :rtype: matplotlib.axes._subplots.Axes3DSubplot
        
    #     """
    #     if ax is None:
    #         fig = plt.figure()
    #         ax = fig.add_subplot(111, projection='3d')
        
        
        
    #     stdict={'Roof':'tab:gray',
    #             'ExteriorWall':'tab:gray',
    #             'Shade':'tab:gray',
    #             'InteriorWall':'tab:cyan',
    #             'InteriorFloor':'tab:gray',
    #             'RaisedFloor':'tab:gray',
    #             'SlabOnGrade':'tab:gray',
    #             'Ceiling':'tab:pink',
    #             'Air':'tab:gray',
    #             'UndergroundSlab':'tab:gray'
    #             }
        
    #     sulines=[]
    #     oplines=[]
    #     verts=[]
    #     edgecolors=[]
    #     facecolors=[]
        
        
    #     for su in self.Surfaces:
            
    #         # if su.surfaceType in ['Roof',
    #         #                       'ExteriorWall',
    #         #                       'Shade',
    #         #                       'SlabOnGrade',
    #         #                       'RaisedFloor'
    #         #                                 ]:
                     
    #         sulines.append(su.get_SimplePolygon().polyline.to_tuple())
    #         pgs=su.get_SimplePolygons_without_openings()
    #         verts.extend([pg.to_tuple() for pg in pgs])
    #         edgecolors.append(stdict[su.surfaceType])
    #         facecolors.append(stdict[su.surfaceType])
            
    #         for op in su.Openings:
                
    #             oplines.append(op.get_SimplePolygon().polyline.to_tuple())
        
    #     # surface polygon fill
    #     ax.add_collection3d(Poly3DCollection(verts,
    #                                          #edgecolors='black',#edgecolors,
    #                                          linewidths=0,
    #                                          facecolors=facecolors,
    #                                          alpha=0.75,
    #                                          **kwargs))
        
    #     # surface perimeter lines
    #     ax.add_collection3d(Line3DCollection(sulines,
    #                                          color='black',
    #                                          alpha=0.5,
    #                                          linewidths=0.25))
        
    #     # opening perimeter lines
    #     ax.add_collection3d(Line3DCollection(oplines,
    #                                          color='tab:gray',
    #                                          linewidths=0.25))
        
        
        
    #     # for su in self.Surfaces:
    #     #     #print(su)
            
    #     #     if not surfaceType is None:
    #     #         #print(su.surfaceType)
    #     #         if not su.surfaceType==surfaceType:
    #     #             continue
            
    #     #     su.plot(ax,
    #     #             set_axis_limits=False,
    #     #             **kwargs)
    #     #     su.PlanarGeometry.PolyLoop.plot(ax,
    #     #                                     linewidth=0.5,
    #     #                                     color='white',
    #     #                                     alpha=0.5)
            
    #         #break
        
    #     x_values,y_values,z_values=[],[],[]
    #     for su in self.Surfaces:
    #         cs=su.get_coordinates()
    #         x_values.extend([c[0] for c in cs])
    #         y_values.extend([c[1] for c in cs])
    #         z_values.extend([c[2] for c in cs])
        
    #     x_range=max(x_values)-min(x_values)
    #     y_range=max(y_values)-min(y_values)
    #     z_range=max(z_values)-min(z_values)
    #     t_range=max([x_range,y_range,z_range])
        
    #     x_mean=(max(x_values)+min(x_values))/2.0
    #     y_mean=(max(y_values)+min(y_values))/2.0
    #     z_mean=(max(z_values)+min(z_values))/2.0
        
    #     ax.set_xlim(x_mean-t_range/2,x_mean+t_range/2)
    #     ax.set_ylim(y_mean-t_range/2,y_mean+t_range/2)
    #     ax.set_zlim(z_mean-t_range/2,z_mean+t_range/2)
        
    #     return ax
        
    
    # def render_surfaces(self,
    #                     scene=None,
    #                     color=vpython.color.blue,
    #                     opacity=0.5
    #                     ):
    #     ""
        
    #     if scene is None:
    #         scene=vpython.canvas(background=vpython.color.gray(0.95))
            
    #         scene.camera.rotate(angle=vpython.pi/2, axis=vpython.vector(1,0,0), origin=vpython.vector(0,0,0))
    #         scene.camera.rotate(angle=vpython.pi/8, axis=vpython.vector(0,0,1), origin=vpython.vector(0,0,0))
            
    #         length=100
            
    #         vpython.arrow(pos=vpython.vector(0,0,0), axis=vpython.vector(length,0,0), shaftwidth=length/100, color=vpython.color.black)
    #         vpython.label( pos=vpython.vec(length+1,0,0), text='X', color=vpython.color.black, box=False , opacity=0)
    #         vpython.arrow(pos=vpython.vector(0,0,0), axis=vpython.vector(0,length,0), shaftwidth=length/100, color=vpython.color.black)
    #         vpython.label( pos=vpython.vec(0,length+1,0), text='Y', color=vpython.color.black, box=False , opacity=0)
    #         vpython.arrow(pos=vpython.vector(0,0,0), axis=vpython.vector(0,0,length+1), shaftwidth=length/100, color=vpython.color.black)
    #         vpython.label( pos=vpython.vec(0,0,length+1), text='Z', color=vpython.color.black, box=False , opacity=0)
        
    
    #     for i, su in enumerate(self.Surfaces):
    #         print(i, end=' ')
    #         try:
    #             su.render(scene=scene)
    #         except: 
    #             print(su)
    
    
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
        return self.Coordinates.value
    
    
    # def get_point(self):
    #     """Returns a Point for the cartesian point.
        
    #     :rtype: crossproduct.Point
        
    #     """
    #     return (*self.get_coordinates())
    
    
    # def plot(self,ax=None,**kwargs):
    #     """Plots the cartesian point
        
    #     :rtype: matplotlib.axes._subplots.Axes3DSubplot
        
    #     """
    #     return self.get_Point().plot(ax=ax,**kwargs)
    
    
    
class ClosedShell():
    ""
    
    # def create_PolyLoops(self,*polyloops_points_coordinates):
    #     """Creates PolyLoop child elements with CartesianPoint and Coordinate subelements.
        
    #     :param polyloop_points_coordinates: An argument list of tuple where each tuple is 
    #         the vertex_values of a PolyLoop.
    #     :type polyloop_points_coordinates: tuple
        
    #     :returns: The newly creeated PolyLoop elements.
    #     :rtype: list(PolyLoop)
        
    #     """
    #     for polyloop_points_coordinates in polyloops_points_coordinates:
    #         self.add_PolyLoop().create_CartesianPoints(*polyloop_points_coordinates)
    #     return self.PolyLoops
        
            
    # def get_coordinates(self):
    #     """Returns the polyloop coordinate values of the PolyLoop child elements.
        
    #     :returns: Polygon values where each value is a tuple of 
    #         the vertex_values of a PolyLoop.
    #     :rtype: tuple(tuple(tuple(float)))
        
    #     """
    #     return tuple([pl.get_coordinates() for pl in self.PolyLoops])



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
    
    
    def get_shell(self):
        """Returns a Polygon of the polyloop child element.
        
        :rtype: tuple
        
        """
        
        return self.PolyLoop.get_shell()
    
    
    def render(self,
               ax=None, 
               set_lims=True, 
               outline_kwargs=None,
               surface_kwargs=None):
        ""
        ax=self.PolyLoop.render(
            ax=ax,
            set_lims=set_lims,
            outline_kwargs=outline_kwargs,
            surface_kwargs=surface_kwargs
            )
        
        return ax
    
    

    # def plot(self,
    #          ax=None,
    #          set_axis_limits=True,
    #          **kwargs):
    #     """Plots the planar geometry.
        
    #     :rtype: matplotlib.axes._subplots.Axes3DSubplot
        
    #     """
    #     sp=self.get_Polygon()
        
    #     if ax is None:
    #         if sp.nD==2:
    #             fig, ax = plt.subplots()
    #         else:
    #             fig = plt.figure()
    #             ax = fig.add_subplot(111, projection='3d')
        
    #     if not 'color' in kwargs:
    #         kwargs['color']='tab:blue'
    #     if not 'alpha' in kwargs:
    #          kwargs['alpha']=0.25
        
    #     ax.add_collection3d(Poly3DCollection([sp.coordinates],
    #                                           **kwargs))
        
    #     if set_axis_limits:
        
    #         x_values=[c[0] for c in sp]
    #         y_values=[c[1] for c in sp]
    #         z_values=[c[2] for c in sp]
            
    #         ax.set_xlim(min(x_values),max(x_values))
    #         ax.set_ylim(min(y_values),max(y_values))
    #         ax.set_zlim(min(z_values),max(z_values))
        
    #     return ax
    
    
    # def render(self,
    #            scene=None,
    #            color=vpython.color.blue,
    #            opacity=0.5
    #            ):
    #     ""
        
    #     pg=self.get_Polygon()
    #     print(pg.bounding_box)
    #     return
        
    #     if scene is None:
    #         scene=vpython.canvas(background=vpython.color.gray(0.95))
            
    #         scene.camera.rotate(angle=vpython.pi/2, axis=vpython.vector(1,0,0), origin=vpython.vector(0,0,0))
    #         scene.camera.rotate(angle=vpython.pi/8, axis=vpython.vector(0,0,1), origin=vpython.vector(0,0,0))
            
    #         # length=max(*pg[0])
            
    #         # vpython.arrow(pos=vpython.vector(0,0,0), axis=vpython.vector(length,0,0), shaftwidth=length/100, color=vpython.color.black)
    #         # vpython.label( pos=vpython.vec(length+1,0,0), text='X', color=vpython.color.black, box=False , opacity=0)
    #         # vpython.arrow(pos=vpython.vector(0,0,0), axis=vpython.vector(0,length,0), shaftwidth=length/100, color=vpython.color.black)
    #         # vpython.label( pos=vpython.vec(0,length+1,0), text='Y', color=vpython.color.black, box=False , opacity=0)
    #         # vpython.arrow(pos=vpython.vector(0,0,0), axis=vpython.vector(0,0,length+1), shaftwidth=length/100, color=vpython.color.black)
    #         # vpython.label( pos=vpython.vec(0,0,length+1), text='Z', color=vpython.color.black, box=False , opacity=0)
        
    #     triangles=pg.triangles
        
    #     render_triangles(triangles,scene,color=color,opacity=opacity)
        
    #     #print(triangles)
    #     #return scene
        
        
    #     return scene
        

# def render_triangles(triangles,scene,**kwargs):
#     ""
#     vtris=[]
#     for t in triangles:
        
#         vs=[vpython.vertex(pos=vpython.vec(*pt),**kwargs) for pt in t]
#         vtri=vpython.triangle(vs=vs)
#         vtris.append(vtri)
        
#     vpython.compound(vtris)
    
#     return scene
    
    

    
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
    
    
    def get_shell(self):
        """
        """
        x = [cp.get_coordinates() for cp in self.CartesianPoints]
        x.append(x[0])
        return tuple(x)
        
    
    
    def render(self,
               ax=None, 
               set_lims=True, 
               outline_kwargs=None,
               surface_kwargs=None):
        ""
        ax=render_functions.render_polygon_3d(
            polygon=(self.get_shell(),[]),
            polygon_triangles=None,
            ax=ax,
            set_lims=set_lims,
            outline_kwargs=outline_kwargs,
            surface_kwargs=surface_kwargs
            )
        
        return ax
    
    
    
    

    # def plot(self,ax=None,**kwargs):
    #     """Plots the polyloop.
        
    #     :rtype: matplotlib.axes._subplots.Axes3DSubplot
        
    #     """
    #     return self.get_SimplePolygon().plot(ax=ax,**kwargs)
    

class RectangularGeometry():
    """
    """
    
    ### needs updating if the RectangularGeometry is for an Opening
    
    def _get_x_vector(self):
        "Returns the 3D vector for the x direction in the rectangular coordinate system"
        azimuth=self.Azimuth.value
        sin_azimuth=math.sin(math.radians(azimuth))
        cos_azimuth=math.cos(math.radians(azimuth))
        return vector_normalize_3d(cos_azimuth,
                                   sin_azimuth,
                                   0)
    
        
    def _get_y_vector(self):
        "Returns the 3D vector for the y direction in the rectangular coordinate system"
        x_vector=self._get_x_vector()
        tilt=self.Tilt.value
        sin_tilt=math.sin(math.radians(tilt))
        cos_tilt=math.cos(math.radians(tilt))
        return vector_normalize_3d(x_vector[0]*cos_tilt,
                                   x_vector[1]*cos_tilt,
                                   sin_tilt)
    
    
    
    def get_shell(self):
        """Returns the coordinates of the rectangular geometry.
        
        The following sources are tried in order:
            - RectangularGeometry/PolyLoop
            - RectangularGeoemetry... from height and width
            
        :rtype: tuple(tuple(float))
            
        """
        try:
            return self.get_shell_from_polyloop()
        except KeyError:
            return self.get_shell_from_height_and_width()
               
    
    
    def get_shell_from_height_and_width(self):
        """Returns the coordintes from the rectangular data using the height and width.
        
        :rtype: tuple(tuple(float))

        """
        if self.getparent().nntag=='Surface':
            
            x_vector=self._get_x_vector()
            y_vector=self._get_y_vector()
            start_point=self.CartesianPoint.get_coordinates()
            height=self.Height.value
            width=self.Width.value        
            
            return (
                vector_addition_3d(*start_point,
                                   *vector_multiplication_3d(*x_vector,
                                                             width)),
                vector_addition_3d(
                    *vector_addition_3d(*start_point,
                                        *vector_multiplication_3d(*x_vector,
                                                                  width)),
                    *vector_multiplication_3d(*y_vector,
                                              height)),
                vector_addition_3d(*start_point,
                                   *vector_multiplication_3d(*y_vector,
                                                             height)),
                start_point,
                vector_addition_3d(*start_point,
                                   *vector_multiplication_3d(*x_vector,
                                                             width))
                )
            
            
        
        else:
            raise Exception('To do')  # i.e. for openings
    
    
    def get_shell_from_polyloop(self):
        """Returns the coordintes from the rectangular data using the polyloop.
        
        :rtype: tuple(tuple(float))

        """
        
        if self.getparent().nntag=='Surface':
            
            x_vector=self._get_x_vector()
            y_vector=self._get_y_vector()
            start_point=self.CartesianPoint.get_coordinates()
            c2d=self.PolyLoop.get_shell()     
            
            return tuple(vector_addition_3d(
                            *vector_addition_3d(*start_point,
                                                *vector_multiplication_3d(*x_vector,
                                                                          c[0])),
                            *vector_multiplication_3d(*y_vector,
                                                      c[1])) 
                        for c in c2d)
    
        else:
            raise Exception('To do')  # i.e. for openings
            
            
    
    def render(self,
               ax=None, 
               set_lims=True, 
               outline_kwargs=None,
               surface_kwargs=None):
        ""
        
        ax=render_functions.render_polygon_3d(
            polygon=(self.get_shell(),[]),
            polygon_triangles=None,
            ax=ax,
            set_lims=set_lims,
            outline_kwargs=outline_kwargs,
            surface_kwargs=surface_kwargs
            )
        
        return ax
            
            
            
    
    # def get_Polygon(self):
    #     """Returns a Polygon of the rectangular eometry.
        
    #     The following sources are tried in order:
    #         - RectangularGeometry/PolyLoop
    #         - RectangularGeometry... from height and width
            
    #     :rtype: crossproduct.Polygon
            
    #     """
    #     return Polygon(*[Point(*c) for c in self.get_coordinates()])
    
    
    # def get_Polygon_from_height_and_width(self):
    #     """Returns a Polygon derived from the rectangular data using the height and width.
        
    #     :rtype: crossproduct.Polygon

    #     """
    #     return Polygon(*[Point(*c) for c in self.get_coordinates_from_height_and_width()])
    
    
    # def get_Polygon_from_polyloop(self):
    #     """Returns a Polygon derived from the rectangular data using the polyloop.
        
    #     The child polyloop data is not used.
        
    #     :rtype: crossproduct.Polygon

    #     """
    #     return Polygon(*[Point(*c) for c in self.get_coordinates_from_polyloop()])



class Space():
    """
    """
    
    
    
class Surface():
    ""


    def get_holes(self):
        """
        """
        return [o.get_shell() for o in self.Openings]
        

    def get_shell(self):
        """Returns a Polygon of the outer polyloop of the opening.
        
        The following sources are tried in order:
            - PlanarGeometry
            - RectangularGeometry/PolyLoop
            - RectangularGeoemetry... from height and width
            
        :rtype: tuple(tuple(float))
            
        """
        try:
            return self.PlanarGeometry.get_shell()
        except KeyError:
            self.RectangularGeometry.get_shell()


    def get_Spaces(self):
        """Returns the space elements adjacent to the surface.
        
        """
        campus=self.getparent()
        return [campus.get_Space(AdjacentSpaceId.spaceIdRef) for AdjacentSpaceId in self.AdjacentSpaceIds]
        
    
    def get_polygon(self):
        """Returns a Polygon of the outer polyloop of the surface.
        
        The following sources are tried in order:
            - PlanarGeometry
            - RectangularGeometry/PolyLoop
            - RectangularGeoemetry... from height and width
            
        :rtype: tuple(tuple(float))
            
        """
        
        return (self.get_shell(), self.get_holes())
    
    
    
    def render(self,
               ax=None, 
               set_lims=True, 
               outline_kwargs=None,
               surface_kwargs=None):
        ""
        
        ax=render_functions.render_polygon_3d(
            polygon=self.get_polygon(),
            polygon_triangles=None,
            ax=ax,
            set_lims=set_lims,
            outline_kwargs=outline_kwargs,
            surface_kwargs=surface_kwargs
            )
        
        for op in self.Openings:
            ax=op.render(ax=ax)
        
        return ax
    
    
    # def plot(self,
    #          ax=None,
    #          wall_color='tab:blue',
    #          roof_color='tab:red',
    #          shade_color='tab:olive',
    #          set_axis_limits=True,
    #          **kwargs):
    #     """Plots the surface.
        
    #     :rtype: matplotlib.axes._subplots.Axes3DSubplot
        
    #     """
    #     if ax is None:
    #         fig = plt.figure()
    #         ax = fig.add_subplot(111, projection='3d')
        
    #     if not 'color' in kwargs:
    #         if self.surfaceType=='Shade':
    #             kwargs['color']=shade_color
    #         elif self.surfaceType=='Roof':
    #             kwargs['color']=roof_color
    #         else:
    #             kwargs['color']=wall_color
    #     if not 'alpha' in kwargs:
    #          kwargs['alpha']=0.25
        
        
        
        
        
    #     sp=self.get_SimplePolygon()
    #     #print(sp)
    #     opening_polygons=[op.get_SimplePolygon() for op in self.Openings]
    #     #print(opening_polygons)
        
    #     # if self.Openings:
    #     #     print(self.id)
    #     #     print(self.Openings)
    #     #     raise Exception
        
    #     if opening_polygons:
    #         #print('test')
    #         #print(self)
    #         dpgs=sp.difference_simple_polygons(opening_polygons)
    #         #print(sp)
    #         #print(opening_polygons)
    #         #print(dpgs)
    #         #print('done')
    #     else:
    #         dpgs=[sp]
        
    #     if len(dpgs)>0:
        
    #         ax.add_collection3d(Poly3DCollection([dpg.to_tuple() for dpg in dpgs],
    #                                              #linewidths=0,
    #                                              **kwargs))
        
    #     # for pg in opening_polygons:
    #     #     pg.plot(ax)
        
        
        
    #     # ax.add_collection3d(Poly3DCollection([sp.to_tuple()],
    #     #                                      **kwargs))
        
    #     if set_axis_limits:
        
    #         x_values=[c[0] for c in sp]
    #         y_values=[c[1] for c in sp]
    #         z_values=[c[2] for c in sp]
            
    #         ax.set_xlim(min(x_values),max(x_values))
    #         ax.set_ylim(min(y_values),max(y_values))
    #         ax.set_zlim(min(z_values),max(z_values))
        
    #     return ax
    
    
    
    # def render(self,
    #            scene=None,
    #            color=vpython.color.blue,
    #            opacity=0.5
    #            ):
    #     ""
        
    #     pgs=[self.get_SimplePolygon()]
        
    #     if scene is None:
    #         scene=vpython.canvas(background=vpython.color.gray(0.95))
            
    #         scene.camera.rotate(angle=vpython.pi/2, axis=vpython.vector(1,0,0), origin=vpython.vector(0,0,0))
    #         scene.camera.rotate(angle=vpython.pi/8, axis=vpython.vector(0,0,1), origin=vpython.vector(0,0,0))
            
    #         length=max(*pgs[0][0])
            
    #         vpython.arrow(pos=vpython.vector(0,0,0), axis=vpython.vector(length,0,0), shaftwidth=length/100, color=vpython.color.black)
    #         vpython.label( pos=vpython.vec(length+1,0,0), text='X', color=vpython.color.black, box=False , opacity=0)
    #         vpython.arrow(pos=vpython.vector(0,0,0), axis=vpython.vector(0,length,0), shaftwidth=length/100, color=vpython.color.black)
    #         vpython.label( pos=vpython.vec(0,length+1,0), text='Y', color=vpython.color.black, box=False , opacity=0)
    #         vpython.arrow(pos=vpython.vector(0,0,0), axis=vpython.vector(0,0,length+1), shaftwidth=length/100, color=vpython.color.black)
    #         vpython.label( pos=vpython.vec(0,0,length+1), text='Z', color=vpython.color.black, box=False , opacity=0)
        
    #     for pg in pgs:
    #         triangles=pg.triangles
    #         l=[]
    #         for t in triangles:
    #             vs=[vpython.vertex(pos=vpython.vec(*pt),
    #                                color=color,
    #                                opacity=opacity) for pt in t]
    #             l.append(vpython.triangle(vs=vs))
    #         vpython.compound(l)
            
    #     return scene
        
    
    
    
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
            self.RectangularGeometry.get_coordinates()
                
                
    def get_shell(self):
        """Returns a Polygon of the outer polyloop of the opening.
        
        The following sources are tried in order:
            - PlanarGeometry
            - RectangularGeometry/PolyLoop
            - RectangularGeoemetry... from height and width
            
        :rtype: tuple(tuple(float))
            
        """
        try:
            return self.PlanarGeometry.get_shell()
        except KeyError:
            self.RectangularGeometry.get_shell()
        
        
    def render(self,
               ax=None, 
               set_lims=True, 
               outline_kwargs=None,
               surface_kwargs=None):
        ""
        x=dict(color='green')
        if outline_kwargs is None:
            outline_kwargs=x
        else:
            for k,v in x.items:
                if not k in outline_kwargs:
                    outline_kwargs[k]=v
            
        x=dict(color='green')
        if surface_kwargs is None:
            surface_kwargs=x
        else:
            for k,v in x.items:
                if not k in surface_kwargs:
                    surface_kwargs[k]=v
        
        ax=render_functions.render_polygon_3d(
            polygon=(self.get_shell(),[]),
            polygon_triangles=None,
            ax=ax,
            set_lims=set_lims,
            outline_kwargs=outline_kwargs,
            surface_kwargs=surface_kwargs
            )
        
        return ax
        
    
    # def plot(self,ax=None,**kwargs):
    #     """Plots the opening.
        
    #     :rtype: matplotlib.axes._subplots.Axes3DSubplot
        
    #     """
    #     return self.get_Polygon().plot(ax=ax,**kwargs)
    
    
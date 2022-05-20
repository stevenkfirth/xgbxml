# -*- coding: utf-8 -*-

import unittest

import xgbxml.geometry_functions as geometry_functions


class Test_Point(unittest.TestCase):
    ""
    
    def test_point_difference_3d(self):
        ""
        self.assertEqual(geometry_functions.point_difference_3d(0,0,0,1,0,0),
                         (1,0,0))
        
    def test_point_project_on_new_coordinate_system_3d(self):
        ""
        x,y,z=0,1,2
        p0=(0,0,0)
        vx_new,vy_new,vz_new=(
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
            (1.0, 0.0, 0.0)
            )      
        
        result=geometry_functions.point_project_on_new_coordinate_system_3d(
            x,y,z,p0,vx_new,vy_new,vz_new
            )
        # print(result)
        
        self.assertEqual(
            result,
            (1.0, 2.0, 0.0)
            )
        
        
    
class Test_Vector(unittest.TestCase):
    ""
    
    def test_vector_collinear_3d(self):
        ""
        v=(1,0,0)
        self.assertTrue(geometry_functions.vector_collinear_3d(*v,*v))
        self.assertFalse(geometry_functions.vector_collinear_3d(*v,*(0,1,0)))
        self.assertTrue(geometry_functions.vector_collinear_3d(*v,*(-1,0,0)))
        
    
    def test_vector_cross_product_3d(self):
        ""
        v,w=(1,0,0),(0,1,0)
        result=geometry_functions.vector_cross_product_3d(*v,*w)
        self.assertEqual(result,(0, 0, 1))
        
        result=geometry_functions.vector_cross_product_3d(*w,*v)
        self.assertEqual(result,(0, 0, -1))
        
        
    def test_vector_index_largest_absolute_coordinate_3d(self):
        ""
        self.assertEqual(geometry_functions.vector_index_largest_absolute_coordinate_3d(1,0,0),
                         0)
        self.assertEqual(geometry_functions.vector_index_largest_absolute_coordinate_3d(0,1,0),
                         1)
        self.assertEqual(geometry_functions.vector_index_largest_absolute_coordinate_3d(0,0,1),
                         2)
        self.assertEqual(geometry_functions.vector_index_largest_absolute_coordinate_3d(-1,0,0),
                         0)
    

    def test_vector_length_3d(self):
        self.assertEqual(geometry_functions.vector_length_3d(2,0,0),
                         2)


    
    
class Test_Plane(unittest.TestCase):
    ""
    
    
        
    def test_plane_almost_equal_3d(self):
        ""
        self.assertTrue(geometry_functions.plane_almost_equal_3d((0,0,0),(0,0,1),(0,0,0),(0,0,1)))
        self.assertTrue(geometry_functions.plane_almost_equal_3d((0,0,0),(0,0,1),(1,1,0),(0,0,1)))
        self.assertTrue(geometry_functions.plane_almost_equal_3d((0,0,0),(0,0,1),(0,0,0),(0,0,-1)))
        self.assertFalse(geometry_functions.plane_almost_equal_3d((0,0,0),(0,0,1),(0,0,0),(1,0,0)))
        self.assertFalse(geometry_functions.plane_almost_equal_3d((0,0,0),(0,0,1),(0,0,1),(0,0,1)))


    def test_plane_new_projection_axes_3d(self):
        ""
        N=(1,0,0)
        
        #vx_new, vy_new, vz_new = geometry_functions.plane_new_axes_3d(N)
        #print((vx_new,vy_new,vz_new))
        
        self.assertEqual(
            geometry_functions.plane_new_projection_axes_3d(N),
            ((0.0, 1.0, 0.0),
             (0.0, 0.0, 1.0),
             (1.0, 0.0, 0.0))                          
            )
        
        
        
    # def test_plane_point_on_axes(self):
    #     ""
    #     return
    #     V0=(0,0,0)
    #     N=(1,0,0)
    #     point=(0,1,2)
    #     v1, v2=geometry_functions.plane_axes_3d(N)
        
    #     self.assertEqual(
    #         geometry_functions.plane_point_on_plane_axes_3d(
    #             V0,N,
    #             point,
    #             v1,v2
    #             ),
    #         (1,2)
    #     )
        


    def test_plane_of_polygon_3d(self):
        ""
        self.assertEqual(
            geometry_functions.plane_of_polygon_3d(
                [(0, 0, 0), 
                 (1, 0, 0), 
                 (1, 0, 1), 
                 (0, 0, 1),
                 (0, 0, 0)]),
                ((0, 0, 0), 
                 (0, -1, 0)
                 )
            )
        
    
    
    
class Test_Polygon(unittest.TestCase):
    ""
    
    # def test_polygon_on_plane_axes_3d(self):
    #     ""
    #     return
    #     shell=((0,0,0),(0,1,0),(0,1,2),(0,0,2),(0,0,0))
    #     holes=[]
    #     #print(geometry_functions.polygon_on_plane_axes_3d(shell, holes))
    #     self.assertEqual(
    #         geometry_functions.polygon_on_plane_axes_3d(shell, holes),
    #         ((0, 0, 0),  # V0
    #          (2, 0, 0),  # N
    #          (0.0, 1.0, 0.0),  # v1 
    #          (0.0, 0.0, 1.0),  # v2 
    #          ((0.0, 0.0), (1.0, 0.0), (1.0, 2.0), (0.0, 2.0), (0.0, 0.0)),  # shell_axes_2d
    #          []  # holes_axes_2d
    #          )
    #         )
        
        
    
    def test_polygon_2d_to_3d(self):
        ""
        plane=(0,0,0),(0,-1,0)
        i=1
        
        # no holes
        shell=((0, 0), (0, 1), (1, 1), (1, 0), (0, 0))
        holes=[]
        self.assertEqual(geometry_functions.polygon_2d_to_3d(i, *plane, shell, holes),
                         (((0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1), (0, 0, 0)),
                          []))
        
        
        # with holes
        shell=((0, 0), (0, 1), (1, 1), (1, 0), (0, 0))
        holes=[[(0.25, 0.25), (0.25, 0.75), 
                (0.75, 0.75), (0.75, 0.25), (0.25, 0.25)]]

        self.assertEqual(geometry_functions.polygon_2d_to_3d(i, *plane, shell, holes),
                         (((0, 0, 0), (1, 0, 0), (1, 0, 1), 
                           (0, 0, 1), (0, 0, 0)),
                          [[(0.25, 0, 0.25), (0.75, 0, 0.25), 
                            (0.75, 0, 0.75), (0.25, 0, 0.75), 
                            (0.25, 0, 0.25)]]))
        
        
        
    def test_polygon_contains_2d(self):
        ""
        pg=([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)], [])
        pg1=([(0, 0), (0.5, 0), (0.5, 1), (0, 1), (0, 0)], [])
        self.assertTrue(geometry_functions.polygon_contains_2d(*pg,*pg1))
        pg2=pg1[0][::-1],[]
        self.assertTrue(geometry_functions.polygon_contains_2d(*pg,*pg2))
    
        
    
    
    def test_polygon_difference_2d(self):
        ""
        
        return  # needs checking
        
        shell1=((0, 0), (0, 1), (1, 1), (1, 0), (0, 0))
        shell2=((0.5, 0), (0.5, 1), (1.5, 1), (1.5, 0), (0.5, 0))
        self.assertEqual(geometry_functions.polygon_difference_2d(shell1, [], 
                                               shell2, []),
                         [(((0.0, 0.0), (0.0, 1.0), (0.5, 1.0), (0.5, 0.0), (0.0, 0.0)), 
                           [])]
                         )
    
    
    def test_polygon_equals_2d(self):
        ""
        pg=([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)], [])
        self.assertTrue(geometry_functions.polygon_equals_2d(*pg,*pg))
        pg1=pg[0][::-1],[]
        self.assertTrue(geometry_functions.polygon_equals_2d(*pg,*pg1))
    
    
    def test_polygon_intersection_overlapping_2d(self):
        ""
        
        return  # needs checking
        
        shell1=((0, 0), (0, 1), (1, 1), (1, 0), (0, 0))
        shell2=((0.5, 0), (0.5, 1), (1.5, 1), (1.5, 0), (0.5, 0))
        self.assertEqual(geometry_functions.polygon_intersection_overlapping_2d(shell1, [], 
                                                             shell2, []),
                         [(((0.5, 1.0), (1.0, 1.0), (1.0, 0.0), (0.5, 0.0), (0.5, 1.0)), 
                           [])]
                         )
    
    
    def test_polygon_intersects_2d(self):
        ""
        pg=([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)], [])
        self.assertTrue(geometry_functions.polygon_intersects_2d(*pg,*pg))
        pg1=pg[0][::-1],[]
        self.assertTrue(geometry_functions.polygon_intersects_2d(*pg,*pg1))
    
    
    
    def test_polygon_overlaps_2d(self):
        ""
        shell=((0, 0), (0, 1), (1, 1), (1, 0), (0, 0))
        
        self.assertFalse(geometry_functions.polygon_overlaps_2d(shell,[],
                                             shell,[])) # exactly equal don't overlap
        self.assertFalse(geometry_functions.polygon_overlaps_2d(shell,[],
                                             ((0.5, 0), (0.5, 1), (1, 1), 
                                              (1, 0), (0.5, 0)),[])) # completely contained within does not overlap
        self.assertTrue(geometry_functions.polygon_overlaps_2d(shell,[],
                                            ((0.5, 0), (0.5, 1), (1.5, 1), 
                                             (1.5, 0), (0.5, 0)),[]))
    
    
   

        
        
    def test_polygon_triangulate_2d(self):
        ""
        tris=geometry_functions.polygon_triangulate_2d(((0,0),(1,0),(1,1),(0,1),(0,0)),[])
        #print(tris)
        self.assertEqual(tris,
                         (((0, 1), (0, 0), (1, 0), (0, 1)), 
                          ((1, 0), (1, 1), (0, 1), (1, 0))))
        
        tris=geometry_functions.polygon_triangulate_2d(((0,0),(1,0),(0,1),(0,0)),[])
        #print(tris)
        self.assertEqual(tris,
                         (((0, 0), (1, 0), (0, 1), (0, 0)),))
        
        
    def test_polygon_triangulate_3d(self):
        ""
        tris=geometry_functions.polygon_triangulate_3d(((0,0,0),(1,0,0),(1,0,1),(0,0,1),(0,0,0)),
                                    [])
        #print(tris)
        self.assertEqual(tris,
                         (((1, 0.0, 0), (0, 0.0, 0), (0, 0.0, 1), (1, 0.0, 0)), 
                          ((0, 0.0, 1), (1, 0.0, 1), (1, 0.0, 0), (0, 0.0, 1))))
        
        
class Test_Polyhedron(unittest.TestCase):
    ""
    
        
    def test_polyhedron_from_base_shell_and_extrud_point_3d(self):
        ""
        base_shell=((0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,0))
        extrud_point=(0,0,1)
        ph=geometry_functions.polyhedron_from_base_shell_and_extrud_point_3d(base_shell,
                                                          extrud_point)
        #print(ph)
        self.assertEqual(len(ph),
                         5)
        
        
        
    def test_polyhedron_from_base_shell_and_extrud_vector_3d(self):
        ""
        base_shell=((0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,0))
        extrud_vector=(0,0,1)
        ph=geometry_functions.polyhedron_from_base_shell_and_extrud_vector_3d(base_shell,extrud_vector)
        #print(ph)
        self.assertEqual(ph,
                         (((0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0), (0, 0, 0)), 
                          ((0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1), (0, 0, 1)), 
                          ((0, 1, 0), (0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 0)), 
                          ((1, 1, 0), (0, 1, 0), (0, 1, 1), (1, 1, 1), (1, 1, 0)), 
                          ((1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1), (1, 0, 0)), 
                          ((0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1), (0, 0, 0))))
        
        
    def test_polyhedron_to_wkt_3d(self):
        ""
        base_shell=((0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,0))
        extrud_vector=(0,0,1)
        ph=geometry_functions.polyhedron_from_base_shell_and_extrud_vector_3d(base_shell,extrud_vector)
        wkt=geometry_functions.polyhedron_to_wkt_3d(ph)
        #print(wkt)
        
        
        

        

        
    

    
    def test_tetrahedron_from_points_3d(self):
        ""
        th=geometry_functions.tetrahedron_from_points_3d((0,0,0),(1,1,0),(0,1,0),(0,1,1))
        self.assertEqual(th,
                         (((0,0,0), (0,1,0), (1,1,0), (0,0,0)),
                          ((0,1,1), (0,1,0), (0,0,0), (0,1,1)),
                          ((0,1,1), (1,1,0), (0,1,0), (0,1,1)),
                          ((0,1,1), (0,0,0), (1,1,0), (0,1,1))))
    

    def test_tetrahedron_volume_3d(self):
        ""
        th=geometry_functions.tetrahedron_from_points_3d((0,0,0),(1,1,0),(0,1,0),(0,1,1))
        self.assertEqual(geometry_functions.tetrahedron_volume_3d(th),
                         0.5*1/3)
                     
    
    def test_tetrahedrons_from_base_shell_and_extrud_vector_3d(self):
        ""
        base_shell=((0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,0))
        extrud_vector=(0,0,1)
        ths=geometry_functions.tetrahedrons_from_base_shell_and_extrud_vector_3d(base_shell,
                                                              extrud_vector)
        #print(ths)
        #print(len(ths))
        self.assertEqual(ths,
                         ((((0, 1, 0.0), (1, 0, 0.0), (0, 0, 0.0), (0, 1, 0.0)), 
                           ((0, 1, 1.0), (1, 0, 0.0), (0, 1, 0.0), (0, 1, 1.0)), 
                           ((0, 1, 1.0), (0, 0, 0.0), (1, 0, 0.0), (0, 1, 1.0)), 
                           ((0, 1, 1.0), (0, 1, 0.0), (0, 0, 0.0), (0, 1, 1.0))), 
                          (((0, 0, 0.0), (0, 1, 1.0), (1, 0, 0.0), (0, 0, 0.0)), 
                           ((0, 0, 1.0), (0, 1, 1.0), (0, 0, 0.0), (0, 0, 1.0)), 
                           ((0, 0, 1.0), (1, 0, 0.0), (0, 1, 1.0), (0, 0, 1.0)), 
                           ((0, 0, 1.0), (0, 0, 0.0), (1, 0, 0.0), (0, 0, 1.0))), 
                          (((0, 1, 1.0), (0, 0, 1.0), (1, 0, 1.0), (0, 1, 1.0)), 
                           ((1, 0, 0.0), (0, 0, 1.0), (0, 1, 1.0), (1, 0, 0.0)), 
                           ((1, 0, 0.0), (1, 0, 1.0), (0, 0, 1.0), (1, 0, 0.0)), 
                           ((1, 0, 0.0), (0, 1, 1.0), (1, 0, 1.0), (1, 0, 0.0))), 
                          (((1, 0, 0.0), (0, 1, 0.0), (1, 1, 0.0), (1, 0, 0.0)), 
                           ((1, 0, 1.0), (0, 1, 0.0), (1, 0, 0.0), (1, 0, 1.0)), 
                           ((1, 0, 1.0), (1, 1, 0.0), (0, 1, 0.0), (1, 0, 1.0)), 
                           ((1, 0, 1.0), (1, 0, 0.0), (1, 1, 0.0), (1, 0, 1.0))), 
                          (((1, 1, 0.0), (1, 0, 1.0), (0, 1, 0.0), (1, 1, 0.0)), 
                           ((1, 1, 1.0), (1, 0, 1.0), (1, 1, 0.0), (1, 1, 1.0)), 
                           ((1, 1, 1.0), (0, 1, 0.0), (1, 0, 1.0), (1, 1, 1.0)), 
                           ((1, 1, 1.0), (1, 1, 0.0), (0, 1, 0.0), (1, 1, 1.0))), 
                          (((1, 0, 1.0), (1, 1, 1.0), (0, 1, 1.0), (1, 0, 1.0)), 
                           ((0, 1, 0.0), (1, 1, 1.0), (1, 0, 1.0), (0, 1, 0.0)), 
                           ((0, 1, 0.0), (0, 1, 1.0), (1, 1, 1.0), (0, 1, 0.0)), 
                           ((0, 1, 0.0), (1, 0, 1.0), (0, 1, 1.0), (0, 1, 0.0)))))
        
        
    def test_tetrahedrons_from_extruded_triangle_3d(self):
        ""
        ths=geometry_functions.tetrahedrons_from_extruded_triangle_3d(((0,0,0),(1,1,0),(0,1,0)),
                                                   (0,0,1))
        self.assertEqual(ths,
                         ((((0, 0, 0), (0, 1, 0), (1, 1, 0), (0, 0, 0)), 
                           ((0, 0, 1), (0, 1, 0), (0, 0, 0), (0, 0, 1)), 
                           ((0, 0, 1), (1, 1, 0), (0, 1, 0), (0, 0, 1)), 
                           ((0, 0, 1), (0, 0, 0), (1, 1, 0), (0, 0, 1))), 
                          (((1, 1, 0), (0, 0, 1), (0, 1, 0), (1, 1, 0)), 
                           ((1, 1, 1), (0, 0, 1), (1, 1, 0), (1, 1, 1)), 
                           ((1, 1, 1), (0, 1, 0), (0, 0, 1), (1, 1, 1)), 
                           ((1, 1, 1), (1, 1, 0), (0, 1, 0), (1, 1, 1))), 
                          (((0, 0, 1), (1, 1, 1), (0, 1, 1), (0, 0, 1)), 
                           ((0, 1, 0), (1, 1, 1), (0, 0, 1), (0, 1, 0)), 
                           ((0, 1, 0), (0, 1, 1), (1, 1, 1), (0, 1, 0)), 
                           ((0, 1, 0), (0, 0, 1), (0, 1, 1), (0, 1, 0)))))
        
        
    def test_tetrahedrons_intersect(self):
        ""
        th=geometry_functions.tetrahedron_from_points_3d((0,0,0),(1,0,0),(0,1,0),(0,0,1))
        th1=geometry_functions.tetrahedron_from_points_3d((0.5,0,0),(1.5,0,0),(0.5,1,0),(0.5,0,1))
        th2=geometry_functions.tetrahedron_from_points_3d((1,0,0),(2,0,0),(1,1,0),(1,0,1))
        th3=geometry_functions.tetrahedron_from_points_3d((1.5,0,0),(2.5,0,0),(1.5,1,0),(1.5,0,1))
        self.assertTrue(geometry_functions.tetrahedrons_intersect(th,th))
        self.assertTrue(geometry_functions.tetrahedrons_intersect(th,th1))
        self.assertFalse(geometry_functions.tetrahedrons_intersect(th,th2))
        self.assertFalse(geometry_functions.tetrahedrons_intersect(th,th3))
    

        
    def test_wkt_to_polyhedron_3d(self):
        ""
        base_shell=((0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,0))
        extrud_vector=(0,0,1)
        ph=geometry_functions.polyhedron_from_base_shell_and_extrud_vector_3d(base_shell,extrud_vector)
        wkt=geometry_functions.polyhedron_to_wkt_3d(ph)
        
        ph1=geometry_functions.wkt_to_polyhedron_3d(wkt)
        #print(ph1)
        
        
    def test_wkt_to_tetrahedron_3d(self):
        ""
        th=geometry_functions.tetrahedron_from_points_3d((0,0,0),(1,1,0),(0,1,0),(0,1,1))
        wkt=geometry_functions.tetrahedron_to_wkt_3d(th)
        
        th1=geometry_functions.wkt_to_tetrahedron_3d(wkt)
        #print(th1)
        


# class Test_Point(unittest.TestCase):
#     ""

#     def test_area(self):
#         ""    
#         point=Point(0,0,0)
#         self.assertEqual(point.area,
#                          0)
        
        
# class Test_Vector(unittest.TestCase):
#     ""
    
    
    
# class Test_Plane(unittest.TestCase):
#     ""
    
#     def test_intersection_plane(self):
#         ""
#         P0,N=Point(0,0,0),Vector(0,0,1)
#         pl=Plane(P0,N)
        
#         # coplanar plane
#         self.assertTrue(pl.intersection(pl).equals(pl))
        
#         # parallel, non-coplanar planes
#         self.assertEqual(pl.intersection(Plane(P0.add(N),N)),
#                          GeometryCollection())
        
#         # intersecting planes - same P0
#         self.assertTrue(pl.intersection(Plane(P0,Vector(1,0,0))).equals(
#                          Line(Point(0,0,0), Vector(0,1,0))))
        
#         self.assertEqual(pl.intersection(Plane(P0,Vector(0,1,0))),
#                          GeometryObjects(Line(Point(0,0,0), Vector(-1,0,0))))
        
#         self.assertEqual(pl.intersection(Plane(P0,Vector(1,1,0))),
#                          GeometryObjects(Line(Point(0,0,0), Vector(-1,1,0))))
        
#         self.assertEqual(pl.intersection(Plane(P0,Vector(0,1,1))),
#                          GeometryObjects(Line(Point(0,0,0), Vector(-1,0,0))))
        
#         # intersecting planes - different P0
#         self.assertEqual(pl.intersection(Plane(P0+ Vector(1,0,0),
#                                          Vector(1,0,0))),
#                          GeometryObjects(Line(Point(1,0,0), Vector(0,1,0))))
        
        
        


# class Test_Polygon(unittest.TestCase):
    
#     def test___init__(self):
#         ""
#         polygon=Polygon([(0, 0, 0), (1, 0, 0), (0, 0, 1)],
#                         holes=[[(0.25, 0, 0.25), (0.75, 0, 0.25), (0.25, 0, 0.75)]])
#         #print(dir(polygon))
#         #print(polygon.representative_point())
#         #print(polygon)
#         #print(polygon.length)
#         #print(polygon.exterior)
#         #print(list(polygon.interiors))
        
    
#     def test_area(self):
#         ""
#         polygon=Polygon([(0, 0, 0), (1, 0, 0), (0, 0, 1)])
#         self.assertEqual(polygon.area,
#                          0)
        
        
#     def test_area3D(self):
#         ""
#         polygon=Polygon([(0, 0, 0), (1, 0, 0), (0, 0, 1)])
#         self.assertEqual(polygon.area3D,
#                          0.5)
        
        
#         polygon=Polygon([(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)],
#                         holes=[[(0.25, 0, 0.25), (0.75, 0, 0.25), 
#                                 (0.75, 0, 0.75), (0.25, 0, 0.75)]])
#         self.assertEqual(polygon.area3D,
#                          0.75)


#     def test_intersection3D(self):
#         ""
#         pg=Polygon(((0,0,0), (1,0,0), (1,1,0), (0,1,0)))
        
#         # in-plane half intersection
#         pg1=Polygon(((0.5,0,0), (1.5,0,0), (1.5,1,0), (0.5,1,0)))
#         #print(pg.intersection(pg1)); return
#         self.assertEqual(pg.intersection3D(pg1),
#                          Polygon(((1,0,0),
#                                   (0.5,0,0),
#                                   (0.5,1,0),
#                                   (1,1,0))))
        


        
#     def test_project2D(self):
#         ""
#         # no holes
#         polygon=Polygon([(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)])
#         plane=polygon.plane
#         i=plane.N.index_largest_absolute_coordinate
#         self.assertEqual(polygon.project_2D(i),
#                          Polygon(((0, 0), (0, 1), (1, 1), (1, 0))))

#         # with holes
#         polygon=Polygon([(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)],
#                         holes=[[(0.25, 0, 0.25), (0.75, 0, 0.25), 
#                                 (0.75, 0, 0.75), (0.25, 0, 0.75)]])
#         plane=polygon.plane
#         i=plane.N.index_largest_absolute_coordinate
#         self.assertEqual(polygon.project_2D(i),
#                          Polygon(((0, 0), (0, 1), (1, 1), (1, 0)),
#                                  holes=[[(0.25, 0.25), (0.25, 0.75), 
#                                          (0.75, 0.75), (0.75, 0.25)]]))
        
        
        
#     def test_project3D(self):
#         ""
#         plane=Plane((0,0,0),(0,-1,0))
#         i=1
        
#         # no holes
#         polygon=Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0)))
#         self.assertEqual(polygon.project_3D(plane, i),
#                          Polygon([(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1), (0, 0, 0)]))
        
#         # with holes
#         polygon=Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0)),
#                         holes=[[(0.25, 0.25), (0.25, 0.75), 
#                                 (0.75, 0.75), (0.75, 0.25), (0.25, 0.25)]])
#         self.assertEqual(polygon.project_3D(plane, i),
#                          Polygon([(0, 0, 0), (1, 0, 0), (1, 0, 1), 
#                                   (0, 0, 1), (0, 0, 0)],
#                                  holes=[[(0.25, 0, 0.25), (0.75, 0, 0.25), 
#                                          (0.75, 0, 0.75), (0.25, 0, 0.75), 
#                                          (0.25, 0, 0.25)]]))
        
                        
                        
        
        

if __name__=='__main__':
    
    
    unittest.main()

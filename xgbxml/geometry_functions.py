# -*- coding: utf-8 -*-

# Some of the algorithms are Python implementations of
# the algorithms provided at this website https://geomalgorithms.com/index.html 
# which requires this notice to be included.
#
# // Copyright 2000 softSurfer, 2012 Dan Sunday
# // This code may be freely used and modified for any purpose
# // providing that this copyright notice is included with it.
# // iSurfer.org makes no warranty for this code, and cannot be held
# // liable for any real or imagined damage resulting from its use.
# // Users of this code must verify correctness for their application.


from shapely.geometry import Polygon, GeometryCollection
import shapely.wkt
import triangle as triangle_package
import math


#%% POINT

def point_2d_to_3d(coordinate_index, V0, N, a1, a2):
        """Projection of a 2D point on a 3D plane.
        
        :param plane: The plane for the projection
        :type plane: Plane
        :param coordinate_index: The index of the coordinate which was ignored 
            to create the 2D projection. For example, coordinate_index=0
            means that the x-coordinate was ignored and this point
            was originally projected onto the yz plane.
        :type coordinate_index: int
        
        :raises ValueError: If coordinate_index is not between 0 and 2.
        
        :return: The 3D point as projected onto the plane.
        :rtype: Point
               
        """
        if coordinate_index==0:
            y=a1
            z=a2
            try:
                x=V0[0]-(N[1]*(y-V0[1])+N[2]*(z-V0[2]))/N[0]
            except ZeroDivisionError:
                raise ValueError('yz points (%s,%s) must exist on the plane.' % (y,z))
        
        elif coordinate_index==1:
            z=a1
            x=a2
            try:
                y=V0[1]-(N[2]*(z-V0[2])+N[0]*(x-V0[0]))/N[1]
            except ZeroDivisionError:
                raise ValueError('zx points (%s,%s) must exist on the plane.' % (z,x))
            
        elif coordinate_index==2:
            x=a1
            y=a2
            try:
                z=V0[2]-(N[0]*(x-V0[0])+N[1]*(y-V0[1]))/N[2]
            except ZeroDivisionError:
                raise ValueError('xy points (%s,%s) must exist on the plane.' % (x,y))
        
        else:
            raise ValueError('coordinate_index must be between 0 and 2')
            
        return x, y, z



def point_3d_to_2d(coordinate_index, a1, a2, a3):
    """Projection of a 3D point as a 2D point.
    
    :param coordinate_index: The index of the coordinate to ignore.
        Use coordinate_index=0 to ignore the x-coordinate, coordinate_index=1 
        for the y-coordinate and coordinate_index=2 for the z-coordinate.
    :type coordinate_index: int
    
    :raises ValueError: If coordinate_index is not between 0 and 2.
    
    :return: A 2D point based on the projection of the 3D point.
    :rtype: Point
           
    """
    if coordinate_index==0:
        return a2, a3
    elif coordinate_index==1:
        return a3, a1
    elif coordinate_index==2:
        return a1, a2
    else:
        raise ValueError('coordinate_index must be between 0 and 2')


def point_difference_3d(a1,a2,a3,b1,b2,b3):
    """Returns the difference between two points, which is a vector
    
    :return vector: the difference of P1 - P0
    :rtype tuple: 
    """
    return b1-a1,b2-a2,b3-a3


def point_project_on_new_coordinate_system_3d(x,y,z,P0_new,vx_new,vy_new,vz_new):
    """Projects a point onto a new coordinate system.
    
    New coordinate system described by origin and three axis vectors.
    
    Returns new x,y,z coordinates for the point.
    
    """
    point=(x,y,z)
    x_new=plane_dist_to_point_3d(point,P0_new,vx_new)[0]
    y_new=plane_dist_to_point_3d(point,P0_new,vy_new)[0]
    z_new=plane_dist_to_point_3d(point,P0_new,vz_new)[0]
    
    return x_new, y_new, z_new
    
    





#%% VECTOR

def vector_angle_3d(v1,v2,v3,w1,w2,w3):
        """Returns the angle between this vector and the supplied vector.
        
        :param vector: A 2D or 3D vector.
        :type vector: Vector
        
        :return: The angle in radians.
        :rtype: float
        
        """
        x=vector_dot_product_3d(v1,v2,v3,w1,w2,w3)
        y=vector_length_3d(v1,v2,v3)
        z=vector_length_3d(w1,w2,w3)
        return math.acos(x/y/z)
    
    
def vector_collinear_3d(v1,v2,v3,w1,w2,w3, abs_tol = 1e-7):
    """Tests if two vectors are collinear.
    
    :returns: True if both vectors are parallel, i.e. they lie on the same line.
        They do not need to be pointing in the same direction. 
        Otherwise returns False.
    :rtype: bool
    
    """
    cp=vector_cross_product_3d(v1,v2,v3,w1,w2,w3)
    vl=vector_length_3d(*cp)
    return math.isclose(vl, 0, abs_tol=abs_tol)
    

def vector_cross_product_3d(v1,v2,v3,w1,w2,w3):
    """Returns the 3D cross product of two vectors
    
    :return vector: the cross product of V0 x V1
    :rtype tuple: 
    """
    return v2*w3-v3*w2,v3*w1-v1*w3,v1*w2-v2*w1   


def vector_dot_product_2d(v1,v2,w1,w2):
    """Returns the dot product of two vectors
    
    :return vector: the dot product of v.w
    :rtype tuple: 
    """
    return v1*w1+v2*w2


def vector_dot_product_3d(v1,v2,v3,w1,w2,w3):
    """Returns the dot product of two vectors
    
    :return vector: the dot product of v.w
    :rtype tuple: 
    """
    return v1*w1+v2*w2+v3*w3


def vector_index_largest_absolute_coordinate_3d(v1, v2, v3):
    """Returns the index of the largest absolute coordinate of the vector.
    
    :return: 0 if the x-coordinate has the largest absolute value, 
        1 if the y-coordinate has the largest absolute value, or
        2 if the z-coordinate has the largest absolute value.
    :rtype: int
    
    """
    absolute_coords=abs(v1), abs(v2), abs(v3)
    return absolute_coords.index(max(absolute_coords)) 


def vector_perp_product_2d(v1,v2,w1,w2):
    """Returns the perp product of two vectors
    
    :return scalar: the perp product of v and w
    :rtype float: 
    """
    return v1*w2-v2*w1


def vector_addition_3d(v1,v2,v3,w1,w2,w3):
    """Returns the sum of two vectors, or a point and a vector
    
    :return vector or point: the sum v + w, or p + v
    :rtype tuple: 
    """
    return v1+w1,v2+w2,v3+w3


def vector_length_2d(v1,v2):
    """Returns the length of a vector
    
    :return length: |v|
    :rtype float:
    """
    return (v1**2+v2**2)**0.5


def vector_length_3d(v1,v2,v3):
    """Returns the length of a vector
    
    :return length: |v|
    :rtype float:
    """
    return (v1**2+v2**2+v3**2)**0.5


def vector_multiplication_3d(v1,v2,v3,a):
    """Returns the multiplication of a vector by a real number
    
    :param a: a real number
    
    :return vector: the multiplication a * v
    :rtype tuple: 
    """
    return a*v1,a*v2,a*v3


def vector_normalize_3d(v1,v2,v3):
    """Returns a normalised vector
    
    :return vector: the normalised vector u for v
    :rtype tuple: 
    """
    length=vector_length_3d(v1,v2,v3)
    return v1/length,v2/length,v3/length
        
        



#%% PLANE

def plane_almost_equal_3d(V0, N, W0, O, abs_tol1=1e-7, abs_tol2=1e-7):
    """Tests if two planes occupy the same space.
    
    plane1 - V0, N
    plane2 - W0, O
    
    :rtype: bool
    
    """
    return (vector_collinear_3d(*N, *O, abs_tol=abs_tol1) 
            and math.isclose(plane_dist_to_point_3d(W0, V0, N)[0],
                             0,
                             abs_tol=abs_tol2))
    

def plane_new_projection_axes_3d(N, abs_tol = 1e-7):
    """Returns three vectors which represent a new set of x,y,z axes.
    
    The plane lies on the new axes where new_z=0.
    
    The vx_new vector is the crossproduct of the plane normal vector and
    the z-axis vector (0,0,1). This vector will therefore have a zero z-component.    
    If the plane normal vector is also (0,0,1),
    then the y-axis vector (0,1,0)  is used instead.
    
    The vy_new is crossproduct of both the vx_new and the plane normal vector.
    
    The vz_new is crossprodut of vx_new and vy_new.
    
    """
    
    # vx_new
    a=vector_cross_product_3d(0, 0, 1, *N)
    if not math.isclose(vector_length_3d(*a),0,abs_tol=abs_tol):
        vx_new=a
    else:
        vx_new=vector_cross_product_3d(0, 1, 0, *N)

    # vy_new
    vy_new=vector_multiplication_3d(*vector_cross_product_3d(*vx_new,*N),
                                -1)
    
    # normalise vectors
    vx_new=vector_normalize_3d(*vx_new)
    vy_new=vector_normalize_3d(*vy_new)
    vz_new=vector_normalize_3d(*N)

    return vx_new, vy_new, vz_new


def plane_dist_to_point_3d(test_point, V0, N):
    """Get distance (and perp base) from a point to a plane
    
    :param test_point: a 3D point
        - i.e. (0,0,0)
    :param V0: a 3D point on the plane
    :param N: a 3D vector which is the normal to the plane
    
    :return result: (the distance from the point to the plane, 
                     the base point on the plane of perpendicular from the test_point)
    :rtype tuple:
    
    """
    sn=-vector_dot_product_3d(*N,*point_difference_3d(*V0,*test_point))
    sd=vector_dot_product_3d(*N,*N)
    sb=sn/sd
    PB = vector_addition_3d(*test_point,*vector_multiplication_3d(*N,sb))
    l=vector_length_3d(*point_difference_3d(*PB,*test_point))
    return l, PB




def plane_of_polygon_3d(shell, abs_tol = 1e-7):
    """Returns the plane of the 3D polygon
    
    :param shell: The exterior coords of the polygon. Start and end coords
        are the same.
    :type shell: list
    
    :return plane: a 3D plane which contains all the polygon points
    :rtype: Plane3D
    
    """
    for i in range(0,len(shell)+1-3):
        c0,c1,c2=shell[i:i+3]
        v1=point_difference_3d(*c0,*c1) #vector_from_points(c0,c1)
        v2=point_difference_3d(*c1,*c2) #vector_from_points(c1,c2)
        N=vector_cross_product_3d(*v1,*v2)
        l=vector_length_3d(*N)
        if not math.isclose(l, 0, abs_tol=abs_tol):
            return (shell[0],N)
    raise ValueError
        
    
# def plane_point_on_plane_axes_3d(V0,N,
#                                  point,
#                                  v1,v2,
#                                  abs_tol = 1e-7):
#     """Returns x and y coordinates of a 3D point on a 3D plane.
    
#     Relative to the plane start point (V0) and the plane v1 and v2 axes.
    
#     :param plane: A plane.
#     :param point: A 3D point on the plane
    
#     v1, v2 from 'plane_axes_3D' method
    
#     :rtype: x, y
    
#     """
#     #print('point',point)
#     #print('v1',v1)
#     #print('v2',v2)
    
#     if plane_dist_to_point_3d(point,V0,N)[0] > abs_tol:
#         raise ValueError('Point does not lie on the plane')

#     x=plane_dist_to_point_3d(point,V0,v1)[0]
#     y=plane_dist_to_point_3d(point,V0,v2)[0]
    
#     #print('x',x)
#     #print('y',y)
    
#     return x, y
    




#%% POLYGON

# def polygon_on_plane_axes_3d(shell, holes):
#     """
#     """
#     V0,N=plane_of_polygon_3d(shell)
#     v1,v2=plane_axes_3d(N)
    
#     shell_axes_2d=[]
#     for point in shell:
#         point_axes_2d=plane_point_on_plane_axes_3d(V0, N, point, v1, v2)
#         shell_axes_2d.append(point_axes_2d)
#     shell_axes_2d=tuple(shell_axes_2d)
        
        
#     holes_axes_2d=[]
#     for hole in holes:
#         x=[]
#         for point in hole:
#             point_axes_2d=plane_point_on_plane_axes_3d(V0, N, point, v1, v2)
#             x.append(point_axes_2d)
#         holes_axes_2d.append(tuple(x))
    
#     return V0, N, v1, v2, shell_axes_2d, holes_axes_2d
    



def polygon_2d_to_3d(coordinate_index, V0, N, shell, holes):
    """
    """
    shell_3d=tuple([point_2d_to_3d(coordinate_index, V0, N, *pt) for pt in shell])
    
    holes_3d=[]
    for hole in holes:
        holes_3d.append([point_2d_to_3d(coordinate_index, V0, N, *pt) 
                         for pt in hole])
    
    return shell_3d, holes_3d   
    

def polygon_3d_to_2d(coordinate_index, shell, holes):
    """
    """
    shell_2d=[point_3d_to_2d(coordinate_index,*pt) for pt in shell]
    
    holes_2d=[]
    for hole in holes:
        holes_2d.append([point_3d_to_2d(coordinate_index,*pt) 
                         for pt in hole])
    
    return shell_2d, holes_2d    


def polygon_area_3d(shell,holes):
    """
    """
    V0,N=plane_of_polygon_3d(shell)
    coordinate_index=vector_index_largest_absolute_coordinate_3d(*N)
    shell_2d,holes_2d=polygon_3d_to_2d(coordinate_index, shell, holes)
    area_2d=Polygon(shell_2d,holes_2d).area
    return abs(area_2d * (vector_length_3d(*N) / N[coordinate_index]))


def polygon_azimuth_3d(shell,holes):
    """The azimuth angle of the polygon from the y axis.
        
    :type polygon: 
    
    :returns: The azimuth angle in degrees where 0 degrees is the direction 
        of the y axis and a positive angle is clockwise.
        If the surface is horizontal, then raises Error.
    :rtype: float
            
    """
    V0,N=plane_of_polygon_3d(shell)
    if vector_collinear_3d(0,0,1,*N):
        raise Exception
    else:
        # working in 2d
        v=N[0],N[1]
        y_axis=(0,1)
        
        # angle between vectors
        angle=math.acos(vector_dot_product_2d(*v,*y_axis)
                        / vector_length_2d(*v)
                        / vector_length_2d(*y_axis))
        angle=math.degrees(angle)
    
        if vector_perp_product_2d(*v,*y_axis)>=0: # if y_axis is on the left of v
            return angle
        else: # y_axis is on the right of v
            return angle * -1


def polygon_bounds_3d(shell,holes):
    """
    """
    xs=[pt[0] for pt in shell]
    ys=[pt[1] for pt in shell]
    zs=[pt[2] for pt in shell]
    
    return min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)


def polygon_centroid_2d(shell,holes):
    """
    """
    return Polygon(shell,holes).centroid.coords[0]


def polygon_centroid_3d(shell,holes):
    """
    """
    V0,N=plane_of_polygon_3d(shell)
    coordinate_index=vector_index_largest_absolute_coordinate_3d(*N)
    shell_2d,holes_2d=polygon_3d_to_2d(coordinate_index, shell, holes)
    pt=polygon_centroid_2d(shell_2d,holes_2d)
    return point_2d_to_3d(coordinate_index, V0, N, *pt)


def polygon_contains_2d(shell1, holes1, 
                        shell2, holes2,
                        ):
    """Tests if one 2D polygon contains the other.
    
    :rtype: bool
    
    """
    return Polygon(shell1, holes1).contains(Polygon(shell2, holes2))
    

def polygon_contains_3d(shell1, holes1, shell2, holes2,
                       abs_tol = 1e-7, abs_tol1=1e-7, abs_tol2=1e-7):
    """Tests if one 2D polygon contains the other.
    
    :rtype: bool
    
    """
    V0,N=plane_of_polygon_3d(shell1, abs_tol=abs_tol)
    W0,O=plane_of_polygon_3d(shell2, abs_tol=abs_tol)
    
    if plane_almost_equal_3d(V0, N, W0, O, abs_tol1=1e-7, abs_tol2=1e-7):
        
        coordinate_index=vector_index_largest_absolute_coordinate_3d(*N)
        shell1_2d,holes1_2d=polygon_3d_to_2d(coordinate_index, shell1, holes1)
        shell2_2d,holes2_2d=polygon_3d_to_2d(coordinate_index, shell2, holes2)
        return polygon_contains_2d(shell1_2d, holes1_2d, 
                                   shell2_2d, holes2_2d)
    
    else:
        
        return False
    

def polygon_difference_2d(shell1, holes1, shell2, holes2):
    """The difference of two 2D polygons
    
    :returns: The coords for the intersection polygons.
        [(shell1, holes1), (shell2, holes2), ...]
    
    
    """
    result=Polygon(shell1, holes1).difference(Polygon(shell2, holes2))
    
    if isinstance(result,Polygon):
        result=GeometryCollection([result])
        
    return [(tuple(pg.exterior.coords), 
             [tuple(lr.coords) for lr in pg.interiors]) 
            for pg in result.geoms]



def polygon_equals_2d(shell1, holes1, 
                      shell2, holes2):
    """Tests if two 2D polygons are equal/equivalent.
    
    Shapely - Returns True if the set-theoretic boundary, interior, and exterior of the object coincide with those of the other.
    
    
    :rtype: bool
    
    """
    return Polygon(shell1, holes1).equals(Polygon(shell2, holes2))


def polygon_equals_3d(shell1, holes1, 
                      shell2, holes2, 
                      abs_tol = 1e-7,
                      abs_tol1=1e-7, abs_tol2=1e-7):
    """Tests if two 2D polygons are equal/equivalent.
    
    :rtype: bool
    
    """
    V0,N=plane_of_polygon_3d(shell1, abs_tol=abs_tol)
    W0,O=plane_of_polygon_3d(shell2, abs_tol=abs_tol)
    
    if plane_almost_equal_3d(V0, N, W0, O, abs_tol1=1e-7, abs_tol2=1e-7):
    
        coordinate_index=vector_index_largest_absolute_coordinate_3d(*N)
        shell1_2d,holes1_2d=polygon_3d_to_2d(coordinate_index, shell1, holes1)
        shell2_2d,holes2_2d=polygon_3d_to_2d(coordinate_index, shell2, holes2)
        return polygon_equals_2d(shell1_2d, holes1_2d, 
                                 shell2_2d, holes2_2d)
    
    else:
        
        return False
   
    
def polygon_intersection_overlapping_2d(shell1, holes1, shell2, holes2):
    """The intersection of two overlapping 2D polygons
    
    :returns: The coords for the intersection polygons.
        [(shell1, holes1), (shell2, holes2), ...].
        Intersection will always be at least one polygon as the initial
        polygons are overlapping.
    
    
    """
    result=Polygon(shell1, holes1).intersection(Polygon(shell2, holes2))
    
    if isinstance(result,Polygon):
        result=GeometryCollection([result])
        
    return [(tuple(pg.exterior.coords), 
             [tuple(lr.coords) for lr in pg.interiors]) 
            for pg in result.geoms]
    

def polygon_intersects_2d(shell1, holes1, shell2, holes2):
    """Tests if two 2D polygons intersect.
    
    From shapely - Returns True if the boundary or interior of the object 
        intersect in any way with those of the other. In other words, 
        geometric objects intersect if they have any boundary or 
        interior point in common.
        
    returns False if the polygons are equal
    
    :rtype: bool
    
    """
    return Polygon(shell1, holes1).intersects(Polygon(shell2, holes2))


def polygon_leftmost_lowest_vertex_index_2D(shell):
    """Returns the index of the leftmost lowest point of the polygon.
    
    :rtype: int
    
       
    """
    
    min_i=0
    for i in range(1,len(shell)):
        if shell[i][1]>shell[min_i][1]:
            continue
        if (shell[i][1]==shell[min_i][1]) and (shell[i][0] > shell[min_i][0]):
            continue
        min_i=i
    return min_i

    
def polygon_overlaps_2d(shell1, holes1, shell2, holes2):
    """Tests if two 2D polygons overlap.
    
    :rtype: bool
    
    """
    return Polygon(shell1, holes1).overlaps(Polygon(shell2, holes2))


def polygon_tilt_3d(shell,holes):
    """The tilt angle of the polygon from the horizontal.
    
    :returns: The tilt angle in degrees where vertically up is 0 degrees and 
        face down is 180 degrees.
    :rtype: float
        
    """
    V0,N=plane_of_polygon_3d(shell)
    z_axis=(0,0,1)
    # angle between vectors
    angle=math.acos(vector_dot_product_3d(*N,*z_axis)
                    / vector_length_3d(*N)
                    / vector_length_3d(*z_axis))
    angle=math.degrees(angle)

    return angle


def polygon_triangulate_2d(shell,holes):
    """Triangulates a 2D polygon 
    
    :returns: A sequence of triangle shells
    :rtype: tuple

    """
    
    vertices=list(shell[:-1])
    for hole in holes:
        vertices.extend(hole[:-1])
    vertices=list(set(vertices))
        
    segments=[]
    for pts in [shell]+holes:
        for i in range(len(pts)-1):
            start_pt_index=vertices.index(pts[i])
            end_pt_index=vertices.index(pts[i+1])
            segments.append((start_pt_index,end_pt_index))
    
    holes=[list(Polygon(x).representative_point().coords[0]) for x in holes]
    #print(holes)
    
    if holes:
        A=dict(vertices=vertices,
               segments=segments,
               holes=holes)
    else:
        A=dict(vertices=vertices,
               segments=segments)
        
    #print(A)
    B=triangle_package.triangulate(A,'p')
    #print(B)
    tris=[]
    for tri in B.get('triangles',[]):
        tris.append((vertices[tri[0]],
                     vertices[tri[1]],
                     vertices[tri[2]],
                     vertices[tri[0]]))
    
    return tuple(tris)
    
    # vertices=shell[:-1]
    # segments=[[x,x+1] for x in range(len(shell)-1)]  # segments index the vertices
    # segments[-1][1]=0
    # A=dict(vertices=vertices,
    #        segments=segments)
    # B=triangle_package.triangulate(A,'p')
    # tris=[]
    # for tri in B.get('triangles',[]):
    #     tris.append((vertices[tri[0]],
    #                  vertices[tri[1]],
    #                  vertices[tri[2]],
    #                  vertices[tri[0]]))
    
    # return tuple(tris)
    

def polygon_triangulate_3d(shell,holes):
    """Triangulates a 3D polygon 
    
    :returns: A sequence of triangle shells
    :rtype: tuple

    """
    V0,N=plane_of_polygon_3d(shell)
    coordinate_index=vector_index_largest_absolute_coordinate_3d(*N)
    shell_2d,holes_2d=polygon_3d_to_2d(coordinate_index, shell, holes)
    tris_2d=polygon_triangulate_2d(shell_2d,holes_2d)
    tris_3d=[]
    for tri_2d in tris_2d:
        tris_3d.append(polygon_2d_to_3d(coordinate_index, V0, N, tri_2d, [])[0])
    return tuple(tris_3d)
    

def polygon_touches_2d(shell1, holes1, shell2, holes2):
    """Tests if two 2D polygons touch.
    
    :rtype: bool
    
    """
    return Polygon(shell1, holes1).touches(Polygon(shell2, holes2))


def polygon_union_2d(shell1, holes1, shell2, holes2):
    """The union of two 2D polygons
    
    :returns: The coords for the union polygons.
        [(shell1, holes1), (shell2, holes2), ...]
    
    
    """

    result=Polygon(shell1, holes1).union(Polygon(shell2, holes2))
    
    if isinstance(result,Polygon):
        result=GeometryCollection([result])
        
    return [(tuple(pg.exterior.coords), 
             [tuple(lr.coords) for lr in pg.interiors]) 
            for pg in result.geoms]




#%% POLYHEDRON


def polyhedron_from_base_shell_and_extrud_point_3d(base_shell, extrud_point):
    """Returns the PolyhedralSurface for the polyhedron
    
    """
    V0,N=plane_of_polygon_3d(base_shell) 
    v=point_difference_3d(*V0,*extrud_point)
    x=vector_dot_product_3d(*N,*v)  # greater than zero if both vectors are pointing on same side of plane
    if x>0:
        base_shell=tuple(list(base_shell)[::-1])  # reverse tr1
    
    #top_shell=tuple([vector_addition_3d(*pt,*extrud_vector) for pt in base_shell[::-1]])
    
    side_shells=[]
    for i in range(len(base_shell)-1):
        sh=tuple((base_shell[i+1],
                  base_shell[i],
                  extrud_point,
                  base_shell[i+1]))
        side_shells.append(sh)
        
    return (base_shell,*side_shells)


def polyhedron_from_base_shell_and_extrud_vector_3d(base_shell, extrud_vector):
    """Returns the PolyhedralSurface for the polyhedron
    
    
    """
    V0,N=plane_of_polygon_3d(base_shell)  # gets the normal of tr1
    x=vector_dot_product_3d(*N,*extrud_vector)  # greater than zero if both vectors are on same side of triangle
    if x>0:
        base_shell=tuple(list(base_shell)[::-1])  # reverse tr1
    
    top_shell=tuple([vector_addition_3d(*pt,*extrud_vector) for pt in base_shell[::-1]])
    
    side_shells=[]
    for i in range(len(base_shell)-1):
        sh=tuple((base_shell[i+1],
                  base_shell[i],
                  vector_addition_3d(*base_shell[i],*extrud_vector),
                  vector_addition_3d(*base_shell[i+1],*extrud_vector),
                  base_shell[i+1]))
        side_shells.append(sh)
        
    return (base_shell,top_shell,*side_shells)
    
    

def polyhedron_to_wkt_3d(polyhedron):
    """
    
    :rtype: str

    """
    x=' '.join(Polygon(pg).wkt for pg in polyhedron)
    x=x[10:]
    x=x.replace(' POLYGON Z',',')
    return 'PolyhedralSurface Z (%s)' % x
    


def tetrahedron_from_points_3d(P0,P1,P2,P3):
    """Forms a tetrahedron from the specified points.
    
    :returns: A tetrahedron.
        All faces of the tetrahedron are 'outward-facing', i.e. their
        normals point to the exterior.
    :rtype: Tetrahedron
    
    """
    # form first 3D triangle
    tr1=((P0,P1,P2,P0))
    
    # is the first triangle 'outward facing'? If not then reverse.
    V0,N=plane_of_polygon_3d(tr1)  # gets the normal of tr1
    v=point_difference_3d(*P0,*P3)  # vector from P0 to P3
    x=vector_dot_product_3d(*N,*v)  # greater than zero if both vectors are on same side of triangle
    if x>0:
        tr1=((P0,P2,P1,P0))  # reverse tr1
        
    V0,N=plane_of_polygon_3d(tr1)  # gets the normal of tr1
        
    tr2=((P3,tr1[1],tr1[0],P3))
    tr3=((P3,tr1[2],tr1[1],P3))
    tr4=((P3,tr1[3],tr1[2],P3))
    
    return (tr1,tr2,tr3,tr4)


def tetrahedron_to_wkt_3d(tetrahedron):
    """
    
    :rtype: str

    """
    x=' '.join(Polygon(tr).wkt for tr in tetrahedron)
    x=x[10:]
    x=x.replace(' POLYGON Z',',')
    return 'Tin Z (%s)' % x


def tetrahedron_volume_3d(tetrahedron):
    """
    tetrahedron: sequence of the face polygons
    """
    # NEEDS testing
    a,b,c,d=list(set(pt for tr in tetrahedron for pt in tr))
    return (abs(vector_dot_product_3d(*point_difference_3d(*d,*a),
                                      *vector_cross_product_3d(*point_difference_3d(*d,*b),
                                                               *point_difference_3d(*d,*c))))
            / 6)


def tetrahedrons_from_base_shell_and_extrud_point_3d(base_shell,
                                                     extrud_point):
    """
    """
    tris=polygon_triangulate_3d(base_shell,[])
    
    ths=[]
    for tri in tris:
        ths.append(tetrahedron_from_points_3d(tri[0],
                                              tri[1],
                                              tri[2],
                                              extrud_point))
    return tuple(ths)

    
def tetrahedrons_from_base_shell_and_extrud_vector_3d(base_shell,
                                                      extrud_vector):
    """
    """
    tris=polygon_triangulate_3d(base_shell,[])
    
    ths=[]
    for tri in tris:
        ths.extend(tetrahedrons_from_extruded_triangle_3d(tri,
                                                          extrud_vector))
    return tuple(ths)
    
    
def tetrahedrons_from_extruded_triangle_3d(triangle, extrud_vector):
    """
    Returns the internal tetrahedrons for an extruded triangle.
    
    """
    
    th0=tetrahedron_from_points_3d(triangle[0],
                                   triangle[1],
                                   triangle[2],
                                   vector_addition_3d(*triangle[0],*extrud_vector))
    th1=tetrahedron_from_points_3d(triangle[1],
                                   triangle[2],
                                   vector_addition_3d(*triangle[0],*extrud_vector),
                                   vector_addition_3d(*triangle[1],*extrud_vector))
    th2=tetrahedron_from_points_3d(vector_addition_3d(*triangle[0],*extrud_vector),
                                   vector_addition_3d(*triangle[1],*extrud_vector),
                                   vector_addition_3d(*triangle[2],*extrud_vector),
                                   triangle[2])
    return (th0,th1,th2)
    

def tetrahedrons_intersect(th1, th2, abs_tol=1e-7):
    """Tests to see if two tetrahedrons intersect
    
    NOTE: Seems to work but not fully tested...
    
    :rtype: bool
    
    """
    th1_points=list(set([pt for tr in th1 for pt in tr]))
    th2_points=list(set([pt for tr in th2 for pt in tr]))
    
    # face planes
    for tr in th1:
        V0,N=plane_of_polygon_3d(tr)
        vs=[point_difference_3d(*V0,*pt) for pt in th2_points]
        x=[vector_dot_product_3d(*v,*N) for v in vs]
        if all((y>0 or math.isclose(y,0,abs_tol=abs_tol)) for y in x):
            return False
        
    for tr in th2:
        V0,N=plane_of_polygon_3d(tr)
        vs=[point_difference_3d(*V0,*pt) for pt in th1_points]
        x=[vector_dot_product_3d(*v,*N) for v in vs]
        if all((y>0 or math.isclose(y,0,abs_tol=abs_tol)) for y in x):
            return False
    
    th1_edges=(point_difference_3d(*th1_points[0],*th1_points[1]),
               point_difference_3d(*th1_points[0],*th1_points[2]),
               point_difference_3d(*th1_points[0],*th1_points[3]),
               point_difference_3d(*th1_points[1],*th1_points[2]),
               point_difference_3d(*th1_points[1],*th1_points[3]),
               point_difference_3d(*th1_points[2],*th1_points[3]))
    th2_edges=(point_difference_3d(*th2_points[0],*th2_points[1]),
               point_difference_3d(*th2_points[0],*th2_points[2]),
               point_difference_3d(*th2_points[0],*th2_points[3]),
               point_difference_3d(*th2_points[1],*th2_points[2]),
               point_difference_3d(*th2_points[1],*th2_points[3]),
               point_difference_3d(*th2_points[2],*th2_points[3]))
                
    # edge planes
    for th1_edge in th1_edges:
        for th2_edge in th2_edges:
            N=vector_cross_product_3d(*th1_edge,*th2_edge)
            
            if not math.isclose(vector_length_3d(*N),0,abs_tol=abs_tol):
            
                # project onto axis
                V0=th1_points[0]
                
                # th1 values
                vs=[point_difference_3d(*V0,*pt) for pt in th1_points]
                x=[vector_dot_product_3d(*v,*N)*vector_length_3d(*v) for v in vs]
                
                # th2 values
                vs=[point_difference_3d(*V0,*pt) for pt in th2_points]
                y=[vector_dot_product_3d(*v,*N)*vector_length_3d(*v) for v in vs]
                
                if ((max(x)<min(y) 
                     or math.isclose(max(x),min(y),abs_tol=abs_tol)) 
                    or (max(y)<min(x) 
                        or math.isclose(max(y),min(x),abs_tol=abs_tol))):
                    return False
                
                # # find V0 in th1 such that th1 is behind the plane
                # for th1_point in th1_points:
                #     vs=[point_difference_3d(*th1_point,*pt) for pt in th1_points]
                #     x=[dot_product_3d(*v,*N) for v in vs]
                #     if all((y<0 or math.isclose(y,0,abs_tol=abs_tol)) for y in x):
                #         V0=th1_point
                #         # is th2 above the plane?
                #         vs=[point_difference_3d(*V0,*pt) for pt in th2_points]
                #         x=[dot_product_3d(*v,*N) for v in vs]
                #         if all((y>0 or math.isclose(y,0,abs_tol=abs_tol)) for y in x):
                #             print(V0,N)
                #             return False
                
                # # find V0 in th2 such that th1 is behind the plane
                # for th2_point in th2_points:
                #     vs=[point_difference_3d(*th2_point,*pt) for pt in th2_points]
                #     x=[dot_product_3d(*v,*N) for v in vs]
                #     if all((y<0 or math.isclose(y,0,abs_tol=abs_tol)) for y in x):
                #         V0=th2_point
                #         # is th1 above the plane?
                #         vs=[point_difference_3d(*V0,*pt) for pt in th1_points]
                #         x=[dot_product_3d(*v,*N) for v in vs]
                #         if all((y>0 or math.isclose(y,0,abs_tol=abs_tol)) for y in x):
                #             return False        
            
    return True
    

    
    



def wkt_to_polyhedron_3d(wkt):
    """
    
    Note: This works, but only just. It'll work if the wkt is created using
        polyhedron_to_wkt_3d.
    
    :rtype: tuple
    
    """
    x=wkt.strip()
    x=x.replace('(((','((')
    x=x.replace('((','Polygon Z ((')
    x=x.replace('PolyhedralSurface Z','GeometryCollection (')
    gc=shapely.wkt.loads(x)
    return tuple(tuple(pg.exterior.coords) for pg in gc.geoms)
        

def wkt_to_tetrahedron_3d(wkt):
    """
    
    Note: This works, but only just. It'll work if the wkt is created using
        tetrahedron_to_wkt_3d.
    
    :rtype: tuple
    
    """
    x=wkt.strip()
    x=x.replace('(((','((')
    x=x.replace('((','Polygon Z ((')
    x=x.replace('Tin Z','GeometryCollection (')
    gc=shapely.wkt.loads(x)
    return tuple(tuple(pg.exterior.coords) for pg in gc.geoms)



# class Point(shapely.geometry.Point):
#     ""
    
#     def add(self,vector):
#         """The addition of this point and a vector.
        
#         :param vector: The vector to be added to the point.
#         :type vector: Vector
        
#         :rtype: Point
        
#         """
#         zipped=itertools.zip_longest(self.coords[0],
#                                      vector.coords[0]) # missing values filled with None
#         try:
#             coordinates=[a+b for a,b in zipped]
#         except TypeError: # occurs if, say, a or b is None
#             raise ValueError('Point and vector to add must be of the same length.')
#         return Point(*coordinates)
    
    
#     def project_2D(self,coordinate_index):
#         """Projection of a 3D point as a 2D point.
        
#         :param coordinate_index: The index of the coordinate to ignore.
#             Use coordinate_index=0 to ignore the x-coordinate, coordinate_index=1 
#             for the y-coordinate and coordinate_index=2 for the z-coordinate.
#         :type coordinate_index: int
        
#         :raises ValueError: If coordinate_index is not between 0 and 2.
        
#         :return: A 2D point based on the projection of the 3D point.
#         :rtype: Point
               
#         """
#         if coordinate_index==0:
#             return Point(self.y,self.z)
#         elif coordinate_index==1:
#             return Point(self.z,self.x)
#         elif coordinate_index==2:
#             return Point(self.x,self.y)
#         else:
#             raise ValueError('coordinate_index must be between 0 and 2')
    
    
#     def project_3D(self,plane,coordinate_index):
#         """Projection of a 2D point on a 3D plane.
        
#         :param plane: The plane for the projection
#         :type plane: Plane
#         :param coordinate_index: The index of the coordinate which was ignored 
#             to create the 2D projection. For example, coordinate_index=0
#             means that the x-coordinate was ignored and this point
#             was originally projected onto the yz plane.
#         :type coordinate_index: int
        
#         :raises ValueError: If coordinate_index is not between 0 and 2.
        
#         :return: The 3D point as projected onto the plane.
#         :rtype: Point
               
#         """
#         if coordinate_index==0:
#             point=plane.point_yz(self.x,self.y)
#         elif coordinate_index==1:
#             point=plane.point_zx(self.x,self.y)
#         elif coordinate_index==2:
#             point=plane.point_xy(self.x,self.y)
#         else:
#             raise ValueError('coordinate_index must be between 0 and 2')
            
#         return point
    
#     def subtract(self,point_or_vector):
#         """Subtraction of supplied object from this point.
        
#         :param point_or_vector: Either a point or a vector.
#         :type point_or_vector: Point or Vector
        
#         :return: If a point is supplied, then a vector is returned (i.e. v=P1-P0). 
#             If a vector is supplied, then a point is returned (i.e. P1=P0-v).
#         :rtype: Point or Vector
        
#         """
#         zipped=itertools.zip_longest(self.coords[0],
#                                      point_or_vector.coords[0]) # missing values filled with None
#         try:
#             coordinates=[a-b for a,b in zipped]
#         except TypeError: # occurs if, say, a or b is None
#             raise ValueError(r'Point and point/vector to subtract must be of the same length.')
#         if isinstance(point_or_vector,Point):
#             return Vector(*coordinates)
#         else:
#             return Point(*coordinates)
    
    
    
    
# class Vector(Point):
#     ""
    
#     def __str__(self):
#         ""
#         return 'VECTOR%s' % str(Point(self))[5:]
    
    
#     def cross_product(self,vector):
#         """Returns the 3D cross product of this vector and the supplied vector.
        
#         :param vector: A 3D vector.
#         :type vector: Vector
        
#         :raises ValueError: If the vector is not a 3D vector.
        
#         :return: The 3D cross product of the two vectors. 
#             This returns a new vector which is perpendicular to 
#             this vector (self) and the supplied vector. 
#             The returned vector has direction according to the right hand rule. 
#             If this vector (self) and the supplied vector are collinear,
#             then the returned vector is (0,0,0)
        
#         :rtype: Vector
        
#         """
#         if self.has_z:
#             v1, v2, v3=self.x, self.y, self.z
#             w1, w2, w3=vector.x, vector.y, vector.z
#             return Vector(v2*w3-v3*w2,
#                           v3*w1-v1*w3,
#                           v1*w2-v2*w1)
#         else:
#             raise ValueError('"cross_product" method can only be used for a 3D vector.')
          
          
#     def dot(self,vector):
#         """Return the dot product of this vector and the supplied vector.
        
#         :param vector: A vector.
#         :type vector: Vector
        
#         :returns: The dot product of the two vectors: 
#             returns 0 if self and vector are perpendicular; 
#             returns >0 if the angle between self and vector is an acute angle (i.e. <90deg); 
#             returns <0 if the angle between self and vector is an obtuse angle (i.e. >90deg).
#         :rtype: float
        
#         """
#         zipped=itertools.zip_longest(self.coords[0],
#                                      vector.coords[0]) # missing values filled with None
#         try:
#             return sum(a*b for a,b in zipped)
#         except TypeError: # occurs if, say, a or b is None
#             raise ValueError(r'Vectors to subtract must be of the same length.')
    
          
            
#     @property
#     def index_largest_absolute_coordinate(self):
#         """Returns the index of the largest absolute coordinate of the vector.
        
#         :return: 1 if the x-coordinate has the largest absolute value, 
#             2 if the y-coordinate has the largest absolute value, or
#             (for 3D vectors) 3 if the z-coordinate has the largest
#             absolute value.
#         :rtype: int
        
#         """
#         absolute_coords=abs(self.x), abs(self.y), abs(self.z)
#         return absolute_coords.index(max(absolute_coords)) 
    
    
#     def is_collinear(self,vector):
#         """Tests if this vector and the supplied vector are collinear.
        
#         :param vector: A vector.
#         :type vector: Vector
        
#         :raise ValueError: If the vector is not 2D or 3D.
        
#         :return: True if the vectors lie on the same line; 
#             otherwise False.
#         :rtype: bool
        
#         """
#         if not self.has_z:
#             return math.isclose(self.perp_product(vector), 0, abs_tol=ABS_TOL)
#         else:
#             return math.isclose(self.cross_product(vector).length, 0, abs_tol=ABS_TOL)
        
    
    
#     def is_perpendicular(self,vector):
#         """Test if this vector and the supplied vector are perpendicular.
        
#         :param vector: A vector.
#         :type vector: Vector
        
#         :return: True if the vectors are perpendicular; 
#             otherwise False.
#         :rtype: bool
        
#         """
#         return math.isclose(self.dot(vector), 0, abs_tol=ABS_TOL)
    
    
#     @property
#     def length(self):
#         """Returns the length of the 2D vector.
        
#         :rtype: float
        
#         """
#         return (self.x**2 + self.y**2)**0.5
    
    
#     @property
#     def length3D(self):
#         ""
#         return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    
#     def perp_product(self,vector):
#         """Returns the perp product of this vector and the supplied vector.
        
#         :param vector: A 2D vector.
#         :type vector: Vector

#         :raises ValueError: If this vector is not a 2D vector.
       
#         :return: The perp product of the two vectors. 
#             The perp product is the dot product of 
#             the perp_vector of this vector and the supplied vector. 
#             If supplied vector is collinear with self, returns 0. 
#             If supplied vector is on the left of self, returns >0 (i.e. counterclockwise). 
#             If supplied vector is on the right of self, returns <0 (i.e. clockwise).
#         :rtype: float
            
#         """
#         if not self.has_z:
#             return self.perp_vector.dot(vector)
#         else:
#             raise ValueError('"perp_product" method only applicable for a 2D vector.')


#     @property
#     def perp_vector(self):
#         """Returns the perp vector of this 2D vector.
        
#         :raises ValueError: If this vector is not a 2D vector.
        
#         :return: The perp vector, i.e. the normal vector on the left 
#             (counterclockwise) side of self.
#         :rtype: Vector
        
#         """
#         if not self.has_z:
#             return Vector(-self.y,self.x)
#         else:
#             raise ValueError('"perp_vector" method only applicable for a 2D vector.')

            
#     def scale(self,scalar):
#         """Multiplication of this vector and a supplied scalar value.
        
#         :param scalar: A numerical scalar value.
#         :type scalar: float
        
#         :rtype: Vector
        
#         """
#         if not self.has_z:
#             return Vector(self.x*scalar, self.y*scalar)            
#         else:
#             return Vector(self.x*scalar, self.y*scalar, self.z*scalar)


#     def subtract(self,vector):
#         """Subtraction of this vector and a supplied vector.
        
#         :param vector: A vector.
#         :type vector: Vector
        
#         :rtype: Vector
        
#         """
        
#         zipped=itertools.zip_longest(self.coords[0],
#                                      vector.coords[0]) # missing values filled with None
#         try:
#             coordinates=[a-b for a,b in zipped]
#         except TypeError: # occurs if, say, a or b is None
#             raise ValueError(r'Vectors to subtract must be of the same length.')
#         return Vector(*coordinates)



# class Line():
#     """
    
#     """
    
#     def __init__(self,P0=None,vL=None):
#         ""
#         self._P0=P0
        
#         if not vL is None:
#             if math.isclose(vL.length, 0, abs_tol=ABS_TOL):
#                 raise ValueError('length of vL must be greater than zero')
#             self._vL=vL    
#         else:
#             self._vL=None
        
        
#     def equals(self,line):
#         """Tests if this line and the supplied line are equal.
        
#         :param line: A line.
#         :type line: Line
        
#         :raises TypeError: If a Line instance is not supplied.
        
#         :return: True if the start point of supplied line lies on line (self),
#             and the vL of supplied line is collinear to the vL of line (self); 
#             otherwise False.
#         :rtype: bool
           
#         """
#         if isinstance(line,Line):
#             return self.intersects(line.P0) and self.vL.is_collinear(line.vL)
#         else:
#             raise TypeError('Line.__eq__ should be used with a Line instance')
    
        
        
#     @property
#     def P0(self):
#         """The starting point of the line.
        
#         :rtype: Point
        
#         """
#         return self._P0
    
    
    
#     @property
#     def vL(self):
#         """The vector of the line.
        
#         :rtype: Vector
        
#         """
#         return self._vL
            
    
    
    
    
# class Plane():
#     ""
    
    
#     def __init__(self,P0=None,N=None):
#         ""
#         if not P0 is None:
#             self._P0=Point(P0)  # should work for either coords or Point
#         else:
#             self._P0=None
#         if not N is None:
#             self._N=Vector(N)  # should work for either coords or Vector
#         else:
#             self._N=None
        
        
#     def __str__(self):
#         ""
#         return 'PLANE (%s, %s)' % (str(self.P0),
#                                    str(self.N))
    
    
#     # def contains(self,obj):
#     #     """Tests if the plane contains the object.
        
#     #     :param obj: A 3D geometric object.
#     #     :type obj: Point, Line
        
#     #     :raises TypeError: If obj is of a type that cannot be contained in a plane.
        
#     #     :rtype: bool
        
        
#     #     """
#     #     if isinstance(obj,Point):
#     #         return self.N.is_perpendicular(obj-self.P0)
#     #     # elif isinstance(obj,Line):
#     #     #    return self.contains(obj.P0) and self.N.is_perpendicular(obj.vL)
#     #     else:
#     #         raise TypeError
    
    
    
    
#     def equals(self,plane):
#         """Tests if this plane and the supplied plane occupy the same geometric space.
        
#         :param plane: A 3D plane.
#         :type plane: Plane
        
#         :return: True if the normal vectors are collinear and 
#             a point can exist on both planes;
#             otherwise False.
#         :rtype: bool
        
#         """
#         if isinstance(plane,Plane):
#             return (self.N.is_collinear(plane.N) 
#                     and math.isclose(abs(self.signed_distance_to_point(plane.P0)),
#                                      0, 
#                                      abs_tol=ABS_TOL))
#         else:
#             return False
    
    
    
#     def intersection(self,obj):
#         """
#         """
#         if isinstance(obj,Plane):
            
#             plane=obj
            
#             if plane.equals(self):
                
#                 return self
            
#             elif plane.N.is_collinear(self.N):
            
#                 return GeometryCollection()  # test with is_empty
            
#             else:
                
#                 n1=self.N
#                 d1=-n1.dot(self.P0.subtract(Point(0,0,0)))
#                 n2=plane.N
#                 d2=-n2.dot(plane.P0.subtract(Point(0,0,0)))
#                 n3=n1.cross_product(n2)
#                 v=n1.scale(d2).subtract(n2.scale(d1))
#                 v1=v.cross_product(n3)
#                 v2=v1.scale((1 / (n3.length3D**2)))
#                 P0=Point(v2.coords[0])
#                 u=n3
#                 return Line(P0,u)
    
#         elif isinstance(obj,Line):
        
#             return self._intersection_line(obj)
        
#         else:
#             raise Exception  # not implemented yet
    
    
#     @property
#     def is_empty(self):
#         ""
#         return self.P0 is None and self.N is None
        
        
        
#     @property
#     def N(self):
#         """The vector normal to the plane.
        
#         :rtype: Vector
        
#         """
#         return self._N
    
    
#     @property
#     def P0(self):
#         """The start point of the plane.
        
#         :rtype: Point
        
#         """
#         return self._P0
        
    
#     def point_xy(self,x,y):
#         """Returns a 3D point on the plane given as x and y coordinates.
        
#         :param x: An x-coordinate.
#         :type x: float
#         :param y: A y-coordinate.
#         :type y: float
        
#         :raises ValueError: If there are no points on the plane with the xy values.
        
#         :rtype: Point
        
#         .. rubric:: Code Example
    
#         .. code-block:: python
           
#            >>> from crossproduct import Point, Vector, Plane
#            >>> pn = Plane(Point(0,0,0), Vector(1,1,1))
#            >>> result = pn.point_xy(1,1)
#            >>> print(result)
#            Point(1.0,1.0,-2.0)
        
#         """
#         try:
#             z=self.P0.z-(self.N.x*(x-self.P0.x)+self.N.y*(y-self.P0.y))/self.N.z
#         except ZeroDivisionError:
#             raise ValueError('xy points (%s,%s) must exist on the plane.' % (x,y))
#         return Point(x,y,z)
    
    
#     def point_yz(self,y,z):
#         """Returns a 3D point on the plane given as y and z coordinates.
        
#         :param y: A y-coordinate.
#         :type y: float
#         :param z: A z-coordinate.
#         :type z: float
        
#         :raises ValueError: If there are no points on the plane with the yz values.
        
#         :rtype: Point
        
#         .. code-block:: python
           
#            >>> from crossproduct import Point, Vector, Plane
#            >>> pn = Plane(Point(0,0,0), Vector(1,1,1))
#            >>> result = pn.point_yz(1,1)
#            >>> print(result)
#            Point(-2.0,1.0,1.0)
        
#         """
#         try:
#             x=self.P0.x-(self.N.y*(y-self.P0.y)+self.N.z*(z-self.P0.z))/self.N.x
#         except ZeroDivisionError:
#             raise ValueError('yz points (%s,%s) must exist on the plane.' % (y,z))
#         return Point(x,y,z)
    
    
#     def point_zx(self,z,x):
#         """Returns a 3D point on the plane given as z and x coordinates.
        
#         :param z: A z-coordinate.
#         :type z: float
#         :param x: An x-coordinate.
#         :type x: float
        
#         :raises ValueError: If there are no points on the plane with the zx values.
        
#         :rtype: Point
        
#         .. rubric:: Code Example
    
#         .. code-block:: python
           
#            >>> from crossproduct import Point, Vector, Plane
#            >>> pn = Plane(Point(0,0,0), Vector(1,1,1))
#            >>> result = pn.point_zx(1,1)
#            >>> print(result)
#            Point(1.0,-2.0,1.0)
        
#         """
#         try:
#             y=self.P0.y-(self.N.z*(z-self.P0.z)+self.N.x*(x-self.P0.x))/self.N.y
#         except ZeroDivisionError:
#             raise ValueError('zx points (%s,%s) must exist on the plane.' % (z,x))
#         return Point(x,y,z)
    
        
#     def signed_distance_to_point(self,point):
#         """Returns the signed distance to the supplied point.
        
#         :param point: A 3D point.
#         :type point:  Point
        
#         :return: The signed distance between the plane and the point.
#             The return value is positive for one side of the plane 
#             (the side in the direction of the normal) and is negative for
#             the other side.
#         :rtype: float
        
           
#         """
#         v=point.subtract(self.P0) # vector_from_points(self.P0,point)
#         return self.N.dot(v) / self.N.length3D

    
    
    
    
# class Polygon(shapely.geometry.Polygon):
#     """Extends the shapely Polygon class
#     """
    
#     @property
#     def area3D(self):
#         ""
#         plane=self.plane
#         N=plane.N
#         i=plane.N.index_largest_absolute_coordinate
#         self_2D=self.project_2D(i)
#         if i==0:
#             return abs(self_2D.area*(N.length/(N.x)))
#         elif i==1:
#             return abs(self_2D.area*(N.length/(N.y)))
#         elif i==2:
#             return abs(self_2D.area*(N.length/(N.z)))
#         else:
#             raise Exception
    
    
#     def intersection(self,obj):
#         ""
#         shapely_polygon=shapely.geometry.Polygon(self)
#         result=shapely_polygon.intersection(obj)
#         return shapely_plus_object_from_shapely_object(result)
    
    
#     def intersection3D(self,obj):
#         """The geometric intersection between self and obj.
        
#         :param obj: A geometric object.
        
#         :returns: A tuple of the difference objects.
#         :rtype: tuple
        
#         """
#         if isinstance(obj,Polygon):
            
#             polygon=obj
#             a=self.plane.intersection(polygon.plane) # returns () or (Line,) or (Plane,)
#             #print(a)
#             if a.is_empty: # polygon planes do not intersect
#                 return Polygon()
            
#             elif isinstance(a,Plane): # polygons lie on the same plane
                
#                 i=self.plane.N.index_largest_absolute_coordinate
#                 self_2D=self.project_2D(i)
#                 polygon_2D=polygon.project_2D(i)
#                 result=self_2D.intersection(polygon_2D)
#                 if isinstance(result,Polygon):
#                     return result.project_3D(self.plane,i)
#                 else:
#                     raise NotImplementedError # to fix for other intersection options
                
                
#             elif isinstance(a,Line): # the intersection of the two polygon planes as a line
                
#                 line=a
#                 x=self.intersection3D(line)
#                 y=polygon.intersection3D(line)
                
#                 result=[]
#                 for x1 in x:
#                     for y1 in y:
#                         result.extend(x1.intersection3D(y1))
                
#                 return shapely.geometry.GeometryCollection(result)
            
#         else:
#             raise NotImplementedError
        
        
#         # if isinstance(obj,Line):
#         #     return self._intersection_line_3D(obj)
#         # elif isinstance(obj,Polygons):
#         #     return self._intersection_polygons_3D(obj)
#         # else:
#         #     raise Exception  # not implemented yet
    
    
    
    
    

#     @property
#     def plane(self):
#         """Returns the plane of the 3D polygon
        
#         :return plane: a 3D plane which contains all the polygon points
#         :rtype: Plane3D
        
#         """
#         if self.has_z:
#             exterior_coords=list(self.exterior.coords)
#             for i in range(0,len(exterior_coords)+1-3):
#                 c0,c1,c2=exterior_coords[i:i+3]
#                 v1=Point(c1).subtract(Point(c0)) #vector_from_points(c0,c1)
#                 v2=Point(c2).subtract(Point(c1)) #vector_from_points(c1,c2)
#                 N=v1.cross_product(v2)
#                 if N.length3D>ABS_TOL:
#                     return Plane(exterior_coords[0],N)
#             raise ValueError
#         else:
#             raise ValueError
        
     
    
            
            
#     def project_2D(self,coordinate_index):
#         """Projects the object on a 2D plane.
        
#         :rtype: Polygon
        
#         """
        
#         def _project_2D_exterior(polygon,coordinate_index):
#             """Returns the exterior of the polygon projected onto a 2D plane.
            
#             :rtype: list (coords)
            
#             """
#             points3D=[Point(x) for x in polygon.exterior.coords]
#             points2D=[x.project_2D(coordinate_index) for x in points3D]
#             return [x.coords[0] for x in points2D]
        
#         exterior_coords2D=_project_2D_exterior(self, coordinate_index)
#         holes_coords2D=\
#             [_project_2D_exterior(Polygon(hole), coordinate_index)
#              for hole in self.interiors]
#         polygon2D=Polygon(exterior_coords2D,
#                           holes=holes_coords2D)
#         return polygon2D
    
    
    
    
    
#     def project_3D(self,plane,coordinate_index):
#         """Projects the 2D polygon on a 3D plane.
        
#         :rype: Polygon
        
#         """
        
#         def _project_3D_exterior(polygon,plane,coordinate_index):
#             """Returns the exterior of the polygon projected onto a 3D plane.
            
#             :rtype: list (coords)
#             """
#             points2D=[Point(x) for x in polygon.exterior.coords]
#             points3D=[x.project_3D(plane,coordinate_index) for x in points2D]
#             return [x.coords[0] for x in points3D]
            
#         exterior_coords3D=_project_3D_exterior(self, plane, coordinate_index)
#         holes_coords3D=\
#             [_project_3D_exterior(Polygon(hole), plane, coordinate_index)
#              for hole in self.interiors]
#         polygon3D=Polygon(exterior_coords3D,
#                           holes=holes_coords3D)
#         return polygon3D
        
        

    
    
    
    
    
# # def vector_from_points(P0,P1):
# #     """Returns the vector from P0 to P1
# #     """
# #     P0=Point(P0)
# #     P1=Point(P1)
# #     return Vector(P1.x-P0.x, P1.y-P0.y, P1.z-P0.z)
    
    
    
# def shapely_plus_object_from_shapely_object(obj):
#     """Converts a shapely object to a shapely_plus object
#     """
    
#     if isinstance(obj,shapely.geometry.Point):
#         return Point(obj)
    
#     elif isinstance(obj,shapely.geometry.Polygon):
#         return Polygon(obj)
    
    
    
#     else:
#         raise NotImplementedError(type(obj))
    
    
    
    
    
# -*- coding: utf-8 -*-
"""
Created on Mon May  9 09:38:15 2022

@author: cvskf
"""

from lxml import etree
import math
from copy import copy

import xgbxml.gbxml_xsd_functions as gbxml_xsd_functions
import xgbxml.xml_functions as xml_functions
import xgbxml.xsd_functions as xsd_functions

from .geometry_functions import vector_normalize_3d, vector_multiplication_3d, vector_addition_3d
import xgbxml.geometry_functions as geometry_functions

ns={'gbxml':'http://www.gbxml.org/schema'}


#%% common

def add_child_to_gbxml_element(gbxml_element,
                               child_nntag,
                               xsd_schema,
                               value=None,
                               **kwargs):
    """Adds a new child element to the element.
    
    :param gbxml_element: A gbXML element.
    :type gbxml_element: lxml.etree._Element
    :param child_nntag: The 'no namespace' tag of the child element (i.e. "Campus")
    :type child_nntag: str
    :param xsd_schema: The root node of a gbXML schema.
    :type xsd_schema: lxml.etree._Element
    :param value: The value for the element. Optional.
    :type value: str, float, bool etc.
    :param kwargs: Attributes to be set for the child element. Optional.
    
    :raises KeyError: If the child name does not exist in the schema.
    :raises: Other error may be raised if the optional value or attributes are
        not specified correctly.
    
    :returns: The newly created child element.
    :rtype: (subclass of) gbElement
    
    """
    element_name=xml_functions.nntag(gbxml_element)
    
    xsd_element=xsd_functions.get_xsd_element_from_xsd_schema(
        xsd_schema=xsd_schema,
        name=element_name)
    
    if not child_nntag \
        in xsd_functions.get_xsd_element_refs_from_xsd_element(xsd_element):
        
        raise KeyError(f'Child name "{child_nntag}" does not exist in schema '
                        + f'for element "{element_name}"')
            
    
    gbxml_element.append(etree.Element('{http://www.gbxml.org/schema}%s' % child_nntag))
    child=gbxml_element.findall('gbxml:%s' % child_nntag,
                                namespaces=ns)[-1]
    if not value is None:
        set_value_of_gbxml_element(gbxml_element=child,
                                   value=value,
                                   xsd_schema=xsd_schema)
        
    for attribute_name,value in kwargs.items():
        if value is not None:
            set_attribute_on_gbxml_element(child,
                                           attribute_name,
                                           value,
                                           xsd_schema)
            
    return child


def get_attribute_of_gbxml_element(gbxml_element,
                                   attribute_name,
                                   xsd_schema):
    """Returns the attribute value of the element.
    
    :param gbxml_element: A gbXML element.
    :type gbxml_element: lxml.etree._Element
    :param attribute_name: The name of the attribute.
    :param attribute_name: str
    :param xsd_schema: The root node of a gbXML schema.
    :type xsd_schema: lxml.etree._Element
        
    :raises KeyError: If the attribute is not present in the element.
    
    :returns: The text value of the attribute converted to the python type
        of the attribute.
    :rtype: bool, str or float etc.
    
    """
    value=gbxml_element.attrib[attribute_name]
    
    element_name=xml_functions.nntag(gbxml_element)
    
    xsd_type=gbxml_xsd_functions.get_xsd_type_of_xsd_attribute(
        element_name,
        attribute_name,
        xsd_schema
        )    
    
    python_type=xsd_functions.xsd_type_to_python_type(xsd_type)
        
    if python_type is bool:
        
        if value=='false':
            return False
        elif value=='true':
            return True
        else:
            raise Exception
        
    elif python_type is str:
        
        return value
    
    elif python_type is int:
        
        return int(value)
    
    elif python_type is float:
        
        return float(value)
        
    else:
        raise Exception


def get_attributes_of_gbxml_element(gbxml_element,
                                    xsd_schema):
    """Returns the attributes of the element.
    
    :param gbxml_element: A gbXML element.
    :type gbxml_element: lxml.etree._Element
    :param xsd_schema: The root node of a gbXML schema.
    :type xsd_schema: lxml.etree._Element
    
    :returns: A dictionary of attributes where the attribute values
        have been converted to the correct python types according to the 
        schema.
    
    :rtype: dict
    
    """
    return {attribute_name:get_attribute_of_gbxml_element(gbxml_element,
                                                          attribute_name,
                                                          xsd_schema) 
            for attribute_name in gbxml_element.attrib}


def get_child_of_gbxml_element(gbxml_element,
                               child_nntag,
                               child_id=None):
    """Returns a child element with specified tag.
    
    If child_id is not supplied, then the first child element found is returned.
    
    :param gbxml_element: A gbXML element.
    :type gbxml_element: lxml.etree._Element
    :param child_nntag: The 'no namespace' tag of the child element (i.e. "Campus")
    :type child_nntag: str
    :param child_id: Optional, the 'id' attribute of the child element.
    :type child_id: str
    
    :raises KeyError: If the child element is not present.
    
    :rtype: (subclass of) gbElement 
    
    """
    element_name=xml_functions.nntag(gbxml_element)
    
    if child_id is None:
        
        result=gbxml_element.find('gbxml:%s' % child_nntag,
                                  namespaces=ns)        
        if result is None:
            raise KeyError(f'Child element with nntag "{child_nntag}" does not exist')
        else:
            return result
    
    else:
        
        result=gbxml_element.find(r'./gbxml:%s[@id="%s"]' % (child_nntag,
                                                             child_id), 
                                  namespaces=ns)
        if result is None:
            raise KeyError(f'Child element with nntag "{child_nntag}" and '
                           + f'id "{child_id}" does not exist' 
                           + f'in element "{element_name}')
        else:
            return result
        
        
def get_children_of_gbxml_element(gbxml_element,
                                  child_nntag):
    """Returns all child element with specified tag.
    
    :param gbxml_element: A gbXML element.
    :type gbxml_element: lxml.etree._Element
    :param child_nntag: The 'no namespace' tag of the child element (i.e. "Campus")
    :type child_nntag: str
    
    :rtype: list
    
    """
    return gbxml_element.findall('gbxml:%s' % child_nntag,
                                  namespaces=ns)  
        

def get_value_of_gbxml_element(gbxml_element,
                               xsd_schema):
    """Returns the value of the gbXML element.
    
    :param gbxml_element: A gbXML element.
    :type gbxml_element: lxml.etree._Element
    :param xsd_schema: The root node of a gbXML schema.
    :type xsd_schema: lxml.etree._Element
    
    :returns: A value which is converted from the element text node.
    :rtype: str, int, float or book etc.
    
    """
    xsd_type=gbxml_xsd_functions.get_xsd_type_of_text_of_xsd_element(
        xml_functions.nntag(gbxml_element),
        xsd_schema
        )
    #print(xsd_type)
    python_type=xsd_functions.xsd_type_to_python_type(xsd_type)
    #print(python_type)
    
    text=gbxml_element.text
    
    return python_type(text)


def set_attribute_on_gbxml_element(gbxml_element,
                                   attribute_name,
                                   value,
                                   xsd_schema):
    """Sets an attribute value of the element.
    
    Attribute will be created if it does not already exist.
    Attribute value is modified if attribute does already exist.
    
    :param gbxml_element: A gbXML element.
    :type gbxml_element: lxml.etree._Element
    :param attribute_name: The name of the attribute.
    :type attribute_name: str
    :param value: The new value for the attribute.
    :type value: bool, str, float
    :param xsd_schema: The root node of a gbXML schema.
    :type xsd_schema: lxml.etree._Element
    
    :raises KeyError: If attribute name does not exist in the schema.
    :raises ValueError: If attribute has enumerations, and 'value' does not
        match one of the enumeration options.
    :raises TypeError: If the attribute value is of a type that does not match 
        the schema.
    
    """
    element_name=xml_functions.nntag(gbxml_element)
    
    xsd_type=gbxml_xsd_functions.get_xsd_type_of_xsd_attribute(
        element_name,
        attribute_name,
        xsd_schema
        )    
    #print(xsd_type)
    
    try:
    
        enumerations=gbxml_xsd_functions.get_enumerations_of_xsd_attribute(
            element_name,
            attribute_name,
            xsd_schema
            )
    
    except Exception:
        
        enumerations=None
        
    #print(enumerations)
        
    if not enumerations is None:
        
        if not value in enumerations:
            raise ValueError(f'Attribute value "{value}" must be one of the '
                             + f'enumerations "{enumerations}".' 
                             + f'({element_name}/@{attribute_name})')
    
    python_type=xsd_functions.xsd_type_to_python_type(xsd_type)
    #print(python_type)
    
    if not isinstance(value,python_type):
        raise TypeError(f'Attribute value {value} has type {type(value)} '
                        + f'which does not match with schema type "{xsd_type}". '
                        + f'({element_name}/@{attribute_name})')
       
    if python_type is str:
        
        value2=str(value)
    
    elif python_type is bool:
        
        if value is True:
            value2='true'
        else:
            value2='false'
        
    else:
        
        raise Exception()
        
    gbxml_element.set(attribute_name,value2)
    
    
    
    
    
def set_value_of_gbxml_element(gbxml_element,
                               value,
                               xsd_schema):
    """Sets the value of the element.
    
    This is stored in the text value of the XML element.
    
    :param gbxml_element: A gbXML element.
    :type gbxml_element: lxml.etree._Element
    :param value: The value for the element.
    :type value: str, float, bool etc.
    :param xsd_schema: The root node of a gbXML schema.
    :type xsd_schema: lxml.etree._Element
    
    :raises TypeError: If value is of a type that does not match 
        the schema.
        
    """
    element_name=xml_functions.nntag(gbxml_element)
    
    xsd_type=gbxml_xsd_functions.get_xsd_type_of_text_of_xsd_element(
        element_name,
        xsd_schema
        )    
    #print(xsd_type)
    
    python_type=xsd_functions.xsd_type_to_python_type(xsd_type)
    #print(python_type)
    
    if not isinstance(value,python_type):
        raise TypeError(f'Value {value} has type {type(value)} '
                        + f'which does not match with schema type "{xsd_type}". '
                        + f'({element_name})')
        
    gbxml_element.text=str(value)
       
    
    
    
    
    



#%% gbXML






#%% Campus






#%% CartesianPoint

def add_Coordinates_to_CartesianPoint(gbxml_element,
                                      xsd_schema,
                                      *coordinates):
    """Creates Coordinate child elements and sets their value.
    
    :param coordinates: The values of the x,y,(z) coordinates as an argument list.
    :type coordinates: int, float
    
    :returns: The newly creeated Coordinate elements.
    :rtype: list(Coordinate)
    
    """
    #print(coordinates)
    
    result=[]
    for coordinate in coordinates:
        x=add_child_to_gbxml_element(gbxml_element,
                                     'Coordinate',
                                     xsd_schema,
                                     value=coordinate)
        result.append(x)
        
    return result
        

def get_Coordinate_values_from_CartesianPoint(gbxml_cartesian_point,
                                              xsd_schema):
    """
    
    :param xsd_schema: schema root node
    
    """
    gbxml_coordinates=get_children_of_gbxml_element(gbxml_cartesian_point,
                                                    'Coordinate')
    
    return tuple(get_value_of_gbxml_element(gbxml_coordinate,
                                            xsd_schema) 
                 for gbxml_coordinate in gbxml_coordinates)
    


#%% PlanarGeometry

def get_coordinate_values_from_PlanarGeometry(gbxml_planar_geometry,
                                              xsd_schema):
    """
    
    :param xsd_schema: schema root node
    
    """
    poly_loop=gbxml_planar_geometry.find('gbxml:PolyLoop',
                                         namespaces=ns)
    return get_coordinate_values_from_PolyLoop(poly_loop,
                                               xsd_schema)


def get_shell_of_PlanarGeometry(gbxml_planar_geometry,
                                xsd_schema):
    """Returns a Polygon of the polyloop child element.
    
    :rtype: tuple
    
    """
    poly_loop=gbxml_planar_geometry.find('gbxml:PolyLoop',
                                         namespaces=ns)
    return get_shell_of_PolyLoop(poly_loop,
                                 xsd_schema)


#%% PolyLoop

def get_coordinate_values_from_PolyLoop(gbxml_poly_loop,
                                        xsd_schema):
    """
    
    :param xsd_schema: schema root node
    
    """
    
    cartesian_points=gbxml_poly_loop.findall('gbxml:CartesianPoint',
                                             namespaces=ns)
    return tuple(get_Coordinate_values_from_CartesianPoint(cp,
                                                           xsd_schema)
                 for cp in cartesian_points)
    

def get_shell_of_PolyLoop(gbxml_poly_loop,
                          xsd_schema):
    """
    """
    x = list(get_coordinate_values_from_PolyLoop(gbxml_poly_loop,
                                                 xsd_schema))
    x.append(x[0])
    return tuple(x)


def set_shell_of_PolyLoop(gbxml_poly_loop,
                          shell,
                          xsd_schema):
    """
    """
    # removes cartesian points
    gbxml_cartesian_points=get_children_of_gbxml_element(gbxml_poly_loop,
                                                         'CartesianPoint')
    for gbxml_cartesian_point in gbxml_cartesian_points:
        gbxml_poly_loop.remove(gbxml_cartesian_point)
    
    # add new cartesian points
    gbxml_cartesian_points=[]
    for xyz in shell[:-1]:
        gbxml_cartesian_point=add_child_to_gbxml_element(gbxml_poly_loop,
                                                         'CartesianPoint',
                                                         xsd_schema)
        add_Coordinates_to_CartesianPoint(gbxml_cartesian_point,
                                          xsd_schema,
                                          *xyz)
        gbxml_cartesian_points.append(gbxml_cartesian_point)
    
    return gbxml_cartesian_points



#%% RectangularGeometry

### needs updating if the RectangularGeometry is for an Opening




def get_shell_of_RectangularGeometry(gbxml_rectangular_geometry,
                                     xsd_schema):
    """Returns the coordinates of the rectangular geometry.
    
    The following sources are tried in order:
        - RectangularGeometry/PolyLoop
        - RectangularGeoemetry... from height and width
        
    :rtype: tuple(tuple(float))
        
    """
    try:
        return get_shell_from_polyloop_of_RectangularGeometry(
            gbxml_rectangular_geometry,
            xsd_schema
            )
    except KeyError:  # is it a KeyError now?
        return get_shell_from_height_and_width_of_RectangularGeometry(
            gbxml_rectangular_geometry,
            xsd_schema
            )
           

def get_shell_from_height_and_width_of_RectangularGeometry(gbxml_rectangular_geometry,
                                                           xsd_schema):
    """Returns the coordintes from the rectangular data using the height and width.
    
    :rtype: tuple(tuple(float))

    """
    if xml_functions.nntag(gbxml_rectangular_geometry.getparent())=='Surface':
        
        x_vector=get_x_vector_of_RectangularGeometry(gbxml_rectangular_geometry,
                                                     xsd_schema)
        y_vector=get_y_vector_of_RectangularGeometry(gbxml_rectangular_geometry,
                                                     xsd_schema)
        start_point=get_Coordinate_values_from_CartesianPoint(
            get_child_of_gbxml_element(gbxml_rectangular_geometry,
                                       'CartesianPoint'),
            xsd_schema
            )
        height=get_Height_value_of_RectangularGeometry(gbxml_rectangular_geometry,
                                                       xsd_schema)
        width=get_Width_value_of_RectangularGeometry(gbxml_rectangular_geometry,
                                                     xsd_schema)      
        
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


def get_shell_from_polyloop_of_RectangularGeometry(gbxml_rectangular_geometry,
                                                   xsd_schema):
    """Returns the coordintes from the rectangular data using the polyloop.
    
    :rtype: tuple(tuple(float))

    """
    
    if xml_functions.nntag(gbxml_rectangular_geometry.getparent())=='Surface':
        
        x_vector=get_x_vector_of_RectangularGeometry(gbxml_rectangular_geometry,
                                                     xsd_schema)
        y_vector=get_y_vector_of_RectangularGeometry(gbxml_rectangular_geometry,
                                                     xsd_schema)
        start_point=get_Coordinate_values_from_CartesianPoint(
            get_child_of_gbxml_element(gbxml_rectangular_geometry,
                                       'CartesianPoint'),
            xsd_schema
            )
        c2d=get_shell_of_PolyLoop(
            get_child_of_gbxml_element(gbxml_rectangular_geometry,
                                       'PolyLoop'),
            xsd_schema
            )
        
        return tuple(vector_addition_3d(
                        *vector_addition_3d(*start_point,
                                            *vector_multiplication_3d(*x_vector,
                                                                      c[0])),
                        *vector_multiplication_3d(*y_vector,
                                                  c[1])) 
                    for c in c2d)

    else:
        raise Exception('To do')  # i.e. for openings
        
        
def get_x_vector_of_RectangularGeometry(gbxml_rectangular_geometry,
                                        xsd_schema):
    "Returns the 3D vector for the x direction in the rectangular coordinate system"
    azimuth=get_Azimuth_value_of_RectangularGeometry(gbxml_rectangular_geometry,
                                                     xsd_schema)
    sin_azimuth=math.sin(math.radians(azimuth))
    cos_azimuth=math.cos(math.radians(azimuth))
    return vector_normalize_3d(cos_azimuth,
                               sin_azimuth,
                               0)

    
def get_y_vector_of_RectangularGeometry(gbxml_rectangular_geometry,
                                        xsd_schema):
    "Returns the 3D vector for the y direction in the rectangular coordinate system"
    x_vector=get_x_vector_of_RectangularGeometry(gbxml_rectangular_geometry,
                                                 xsd_schema)
    tilt=get_Tilt_value_of_RectangularGeometry(gbxml_rectangular_geometry,
                                               xsd_schema)
    sin_tilt=math.sin(math.radians(tilt))
    cos_tilt=math.cos(math.radians(tilt))
    return vector_normalize_3d(x_vector[0]*cos_tilt,
                               x_vector[1]*cos_tilt,
                               sin_tilt)


def get_Azimuth_value_of_RectangularGeometry(gbxml_rectangular_geometry,
                                             xsd_schema):
    ""
    gbxml_azimuth=get_child_of_gbxml_element(gbxml_rectangular_geometry,
                                             'Azimuth')
    return get_value_of_gbxml_element(gbxml_azimuth,
                                      xsd_schema)


def get_Height_value_of_RectangularGeometry(gbxml_rectangular_geometry,
                                            xsd_schema):
    ""
    gbxml_height=get_child_of_gbxml_element(gbxml_rectangular_geometry,
                                            'Height')
    return get_value_of_gbxml_element(gbxml_height,
                                      xsd_schema)


def get_Tilt_value_of_RectangularGeometry(gbxml_rectangular_geometry,
                                          xsd_schema):
    ""
    gbxml_tilt=get_child_of_gbxml_element(gbxml_rectangular_geometry,
                                          'Tilt')
    return get_value_of_gbxml_element(gbxml_tilt,
                                      xsd_schema)


def get_Width_value_of_RectangularGeometry(gbxml_rectangular_geometry,
                                           xsd_schema):
    ""
    gbxml_width=get_child_of_gbxml_element(gbxml_rectangular_geometry,
                                           'Width')
    return get_value_of_gbxml_element(gbxml_width,
                                      xsd_schema)


#%% Surface


def copy_Opening_to_Surface(gbxml_opening,
                            gbxml_surface,
                            xsd_schema,
                            tolerance=0.01
                            ):
    """Adds an existing opening to an existing surface.
    
    
    :param tolerance: The distance which an opening can be 'snapped' to a surface.
    
    
    """
    
    #return
    
    surface_shell=get_shell_of_Surface(gbxml_surface,
                                       xsd_schema)  # tuple
    #print('surface_shell', surface_shell)
    surface_plane=geometry_functions.plane_of_polygon_3d(surface_shell)  # (V,N)
    #print(surface_plane)
    
    opening_shell=get_shell_of_Opening(gbxml_opening,
                                       xsd_schema)
    
    #print('opening_shell',opening_shell)
    
    opening_shell_on_plane=[]
    for xyz in opening_shell:
        distance, base_point=geometry_functions.dist_point_to_plane_3d(
            xyz,
            *surface_plane
            )
        
        if distance>tolerance:
            raise ValueError('Distance between Opening and Surface is greater than the tolerance value')
        
        opening_shell_on_plane.append(base_point)
        
    #print('opening_shell_on_plane',opening_shell_on_plane)
    
    # check if opening shell is contained by the surface shell + holes
    
    surface_holes=get_holes_of_Surface(gbxml_surface,
                                       xsd_schema)
    #print('surface_holes',surface_holes)
    
    if not geometry_functions.polygon_contains_3d(surface_shell, 
                                                  surface_holes, 
                                                  opening_shell_on_plane, 
                                                  []
                                                  ):
        raise ValueError('New opening does not fit onto surface')
    
    
    
    gbxml_opening2=copy(gbxml_opening)
    
    set_shell_of_Opening(gbxml_opening2,
                         opening_shell_on_plane,
                         xsd_schema)
    
    gbxml_surface.append(gbxml_opening2)
    
    
    return gbxml_opening2
    
    
    
    
    
    


def get_holes_of_Surface(gbxml_surface,
                         xsd_schema):
    """
    """
    return [get_shell_of_Opening(gbxml_opening,
                                 xsd_schema) 
            for gbxml_opening in get_children_of_gbxml_element(gbxml_surface, 
                                                               'Opening')]
    

def get_shell_of_Surface(gbxml_surface,
                         xsd_schema):
    """Returns a Polygon of the outer polyloop of the opening.
    
    The following sources are tried in order:
        - PlanarGeometry
        - RectangularGeometry/PolyLoop
        - RectangularGeoemetry... from height and width
        
    :rtype: tuple(tuple(float))
        
    """
    try:
        gbxml_planar_geometry=get_child_of_gbxml_element(gbxml_surface,
                                                         'PlanarGeometry')
        return get_shell_of_PlanarGeometry(gbxml_planar_geometry,
                                           xsd_schema)
    except KeyError:
        gbxml_rectangular_geometry=get_child_of_gbxml_element(gbxml_surface,
                                                              'RectangularGeometry')
        return get_shell_of_RectangularGeometry(gbxml_rectangular_geometry,
                                                xsd_schema)


def get_Spaces_of_Surface(gbxml_surface):
    """Returns the space elements adjacent to the surface.
    
    """
    campus=gbxml_surface.getparent()
    return [campus.xpath('.//Space[@id="%s"]' % AdjacentSpaceId,
                         namespaces=ns)[0]
            for AdjacentSpaceId in get_children_of_gbxml_element(gbxml_surface,
                                                                 'AdjacentSpaceIds')]


def get_polygon_of_Surface(gbxml_surface,
                           xsd_schema):
    """Returns a Polygon of the outer polyloop of the surface.
    
    The following sources are tried in order:
        - PlanarGeometry
        - RectangularGeometry/PolyLoop
        - RectangularGeoemetry... from height and width
        
    :rtype: tuple(tuple(float))
        
    """
    
    return (get_shell_of_Surface(gbxml_surface,
                                 xsd_schema), 
            get_holes_of_Surface(gbxml_surface,
                                 xsd_schema))



#%% Opening




    
               
def get_shell_of_Opening(gbxml_opening,
                         xsd_schema):
    """Returns a Polygon of the outer polyloop of the opening.
    
    The following sources are tried in order:
        - PlanarGeometry
        - RectangularGeometry/PolyLoop
        - RectangularGeoemetry... from height and width
        
    :rtype: tuple(tuple(float))
        
    """
    try:
        gbxml_planar_geometry=get_child_of_gbxml_element(gbxml_opening,
                                                         'PlanarGeometry')
        return get_shell_of_PlanarGeometry(gbxml_planar_geometry,
                                           xsd_schema)
    except KeyError:
        gbxml_rectangular_geometry=get_child_of_gbxml_element(gbxml_opening,
                                                              'RectangularGeometry')
        return get_shell_of_RectangularGeometry(gbxml_rectangular_geometry,
                                                xsd_schema)
    
    

def set_shell_of_Opening(gbxml_opening,
                         shell,
                         xsd_schema):
    """
    """
    # removes rectangular geometry
    try:
        gbxml_rectangular_geometry=get_child_of_gbxml_element(gbxml_opening,
                                                               'RectangularGeometry')
        gbxml_opening.remove(gbxml_rectangular_geometry)
    except KeyError:
        pass
    
    # removes planar geometry
    try:
        gbxml_planar_geometry=get_child_of_gbxml_element(gbxml_opening,
                                                               'PlanarGeometry')
        gbxml_opening.remove(gbxml_planar_geometry)
    except KeyError:
        pass
    
    # adds new elements
    gbxml_planar_geometry=add_child_to_gbxml_element(gbxml_opening,
                                                     'PlanarGeometry',
                                                     xsd_schema)
    gbxml_poly_loop=add_child_to_gbxml_element(gbxml_planar_geometry,
                                               'PolyLoop',
                                               xsd_schema)
    
    set_shell_of_PolyLoop(gbxml_poly_loop,
                          shell,
                          xsd_schema)

    #print(etree.tostring(copy(gbxml_opening),pretty_print=True).decode())
    
    return gbxml_planar_geometry
    
    
    
    
    
    
    

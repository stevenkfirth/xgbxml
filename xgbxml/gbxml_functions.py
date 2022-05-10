# -*- coding: utf-8 -*-
"""
Created on Mon May  9 09:38:15 2022

@author: cvskf
"""

from lxml import etree

import xgbxml.gbxml_xsd_functions as gbxml_xsd_functions
import xgbxml.xml_functions as xml_functions

ns={'gbxml':'http://www.gbxml.org/schema'}


#%% common

def add_child_to_gbxml_element(gbxml_element,
                               child_nntag,
                               xsd_schema,
                               text=None,
                               **kwargs):
    """Adds a new child element to the element.
    
    :param child_nntag: The 'no namespace' tag of the child element.
    :type child_nntag: str
    :param kwargs: Attributes to be set for the child element.
    
    :returns: The newly created child element.
    :rtype: (subclass of) gbElement
    
    """
    gbxml_element.append(etree.Element('{http://www.gbxml.org/schema}%s' % child_nntag))
    child=gbxml_element.findall('gbxml:%s' % child_nntag,
                                namespaces=ns)[-1]
    if not text is None:
        child.text=text
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
    """Returns the attribute value as a python type.
    
    :param attribute_name: The name of the attribute.
    :param attribute_name: str
    
    :raises KeyError: If the attribute is not present in the element.
    
    :rtype: bool, str, float
    
    """
    value=gbxml_element.attrib[attribute_name]
    
    element_name=xml_functions.nntag(gbxml_element)
    
    xsd_type=gbxml_xsd_functions.get_xsd_type_of_xsd_attribute(
        element_name,
        attribute_name,
        xsd_schema
        )    
    
    python_type=xml_functions.xsd_type_to_python_type(xsd_type)
        
    if python_type is bool:
        
        if value=='false':
            return False
        elif value=='true':
            return True
        else:
            raise Exception
        
    elif python_type is str:
        
        return value
        
    else:
        raise Exception


def get_attributes_of_gbxml_element(gbxml_element,
                                    xsd_schema):
    """The attributes of the element.
    
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
    
    :param child_nntag: The 'no namespace' tag of the child element.
    :type child_nntag: str
    :param child_id: Optional, the 'id' attribute of the child element.
    :type child_id: str
    
    :raises ??: If the child element is not present.
    
    :rtype: (subclass of) gbElement 
    
    """
    if child_id is None:
        
        result=gbxml_element.find('gbxml:%s' % child_nntag,
                                  namespaces=ns)        
        if result is None:
            raise KeyError('Child element with nntag "%s" does not exist' % child_nntag)
        else:
            return result
    
    else:
        
        result=gbxml_element.find(r'./gbxml:%s[@id="%s"]' % (child_nntag,
                                                             child_id), 
                                  namespaces=ns)
        if result is None:
            raise KeyError('Child element with nntag "%s" and id "%s" does not exist' % (child_nntag,
                                                                                         child_id))
        else:
            return result
        
        


def set_attribute_on_gbxml_element(gbxml_element,
                                   attribute_name,
                                   value,
                                   xsd_schema):
    """Sets an attribute value of the element.
    
    Attribute will be created if it does not already exist.
    Attribute value is modified if attribute does already exist.
    Value is coerced to the correct python type if needed.
    
    :param attribute_name: The name of the attribute.
    :param attribute_name: str
    :param value: The new value for the attribute.
    :type value: bool, str, float
    
    :raises KeyError: If attribute does not exist in the schema.
    :raises ValueError: If attribute has enumerations, and 'value' does not
        match one of the enumeration options.
    
    :rtype: The (coerced) value assigned to the attribute.
    
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
            raise ValueError('Attribute value "%s" must be one of the enumerations' % value)
    
    python_type=xml_functions.xsd_type_to_python_type(xsd_type)
    #print(python_type)
       
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
    
    return value2
    
    
    



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
                                     text=str(coordinate))
        result.append(x)
        
    return result
        
    


def get_Coordinate_values_from_CartesianPoint(gbxml_cartesian_point,
                                              xsd_schema):
    """
    
    :param xsd_schema: schema root node
    
    """
    x=gbxml_cartesian_point.xpath('./gbxml:Coordinate/text()',
                                  namespaces=ns)
    #print(x)
    xsd_type=gbxml_xsd_functions.get_xsd_type_of_text_of_xsd_element(
        'Coordinate',
        xsd_schema
        )
    #print(xsd_type)
    python_type=xml_functions.xsd_type_to_python_type(xsd_type)
    #print(python_type)
    
    return tuple(python_type(y) for y in x)


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


#%% RectangularGeometry



#%% Surface


#%% Opening
    
    
    
    
    
    
    
    
    
    

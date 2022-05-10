# -*- coding: utf-8 -*-
"""
Created on Mon May  9 13:55:41 2022

@author: cvskf
"""

from .xsd_functions import *
from lxml import etree
from copy import copy


#%% xsd_attribute

def get_xsd_type_of_xsd_attribute(element_name,
                                  attribute_name,
                                  xsd_schema):
    """
    """
    xsd_element=get_xsd_element_from_xsd_schema(xsd_schema,
                                                name=element_name)
    
    xsd_attribute=get_xsd_attribute_from_xsd_element(xsd_element,
                                                      attribute_name)
    
    type_=get_type_from_xsd_attribute(xsd_attribute)
    
    if isinstance(type_,str):
        
        try:
            type_=get_xsd_simple_type_from_xsd_schema(xsd_schema,
                                                      name=type_)
        except Exception:
            return type_
    
    # assume now that type_ is a simpleType
    
    return get_restriction_base_from_xsd_simple_type(type_)

    
    
def get_enumerations_of_xsd_attribute(element_name,
                                      attribute_name,
                                      xsd_schema):
    """
    """

    xsd_element=get_xsd_element_from_xsd_schema(xsd_schema,
                                                name=element_name)
    
    xsd_attribute=get_xsd_attribute_from_xsd_element(xsd_element,
                                                      attribute_name)
    
    type_=get_type_from_xsd_attribute(xsd_attribute)
    
    if isinstance(type_,str):
        
        try:
            type_=get_xsd_simple_type_from_xsd_schema(xsd_schema,
                                                      name=type_)
        except Exception:
            raise Exception
    
    # assume now that type_ is a simpleType
    
    return get_restriction_enumeration_values_from_xsd_simple_type(type_)




#%% xsd_element

def get_xsd_type_of_text_of_xsd_element(name,xsd_schema):
    """
    """
    xsd_element=get_xsd_element_from_xsd_schema(xsd_schema,name)
    
    #print(etree.tostring(copy(xsd_element)).decode())
    
    type_=get_type_from_xsd_element(xsd_element)
    
    if isinstance(type_,str):
        return type_
    
    elif type_.tag=='{http://www.w3.org/2001/XMLSchema}simpleType':
        
        return get_restriction_base_from_xsd_simple_type(type_)
        
        
    elif type_.tag=='{http://www.w3.org/2001/XMLSchema}complexType':
    
        xsd_simple_content=get_xsd_simple_content_from_xsd_complex_type(type_)
        return get_xsd_extension_base_from_xsd_simple_content(xsd_simple_content)
    
    else:
        raise Exception
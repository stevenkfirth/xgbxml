# -*- coding: utf-8 -*-
"""
Created on Mon May  9 12:01:45 2022

@author: cvskf
"""

ns={'xsd':"http://www.w3.org/2001/XMLSchema"}


#%% xsd_attribute

def get_type_from_xsd_attribute(xsd_attribute):
    """
    
    :rtype: str, or element (i.e. xsd:SimpleType)
    
    """
    try:
        return xsd_attribute.attrib['type']
    except KeyError:
        pass
    
    try:
        return xsd_attribute.xpath('./xsd:simpleType',
                                   namespaces=ns)[0]
    except IndexError:
        pass
    
    raise Exception
    
    
#%% xsd_complex_type

def get_xsd_simple_content_from_xsd_complex_type(xsd_complex_type):
    """
    """
    try:
        return xsd_complex_type.xpath('./xsd:simpleContent',
                                      namespaces=ns)[0]
    except IndexError:
        raise Exception
    
    

#%% xsd_element

def get_xsd_attribute_from_xsd_element(xsd_element,
                                       name):
    """
    """
    try:
        return xsd_element.xpath('.//xsd:attribute[@name="%s"]' % name, 
                                 namespaces=ns)[0]
    except IndexError:
        raise Exception
        
        
def get_xsd_attribute_names_from_xsd_element(xsd_element):
    """
    """
    attributes=get_xsd_attributes_from_xsd_element(xsd_element)
    return [x.attrib['name'] for x in attributes]
        
        
def get_xsd_attributes_from_xsd_element(xsd_element):
    """
    """
    return xsd_element.xpath('.//xsd:attribute', 
                             namespaces=ns)
    

def get_type_from_xsd_element(xsd_element):
    """
    
    :rtype: str, or element (i.e. xsd:SimpleType or xsd:ComplexType)
    
    """
    try:
        return xsd_element.attrib['type']
    except KeyError:
        pass
    
    try:
        return xsd_element.xpath('./xsd:simpleType',
                                   namespaces=ns)[0]
    except IndexError:
        pass
    
    try:
        return xsd_element.xpath('./xsd:complexType',
                                   namespaces=ns)[0]
    except IndexError:
        pass
    
    raise Exception

    
    
#%% xsd_schema

def get_xsd_element_from_xsd_schema(xsd_schema,name):
    """
    """
    
    gen=xsd_schema.iterchildren('{http://www.w3.org/2001/XMLSchema}element')
    for xsd_element in gen:
        if xsd_element.attrib['name']==name:
            return xsd_element
    raise Exception
    
    
        
def get_xsd_simple_type_from_xsd_schema(xsd_schema,name):
    """
    """
    gen=xsd_schema.iterchildren('{http://www.w3.org/2001/XMLSchema}simpleType')
    for xsd_simple_type in gen:
        if xsd_simple_type.attrib['name']==name:
            return xsd_simple_type
    raise Exception
    
    

    
#%% xsd_simple_content

def get_xsd_extension_from_xsd_simple_content(xsd_simple_content):
    """
    """
    try:
        return xsd_simple_content.xpath('./xsd:extension',
                                        namespaces=ns)[0]
    except IndexError:
        raise Exception
    
def get_xsd_extension_base_from_xsd_simple_content(xsd_simple_content):
    """
    """
    extension=get_xsd_extension_from_xsd_simple_content(xsd_simple_content)
    return extension.attrib['base']
    
    
    
#%% xsd_simple_type

def get_restriction_from_xsd_simple_type(xsd_simple_type):
    """
    """
    try:
        return xsd_simple_type.xpath('./xsd:restriction',
                                     namespaces=ns)[0]
    except IndexError:
        raise Exception


def get_restriction_base_from_xsd_simple_type(xsd_simple_type):
    """
    """
    restriction=get_restriction_from_xsd_simple_type(xsd_simple_type)
    return restriction.attrib['base']
    

def get_restriction_enumeration_values_from_xsd_simple_type(xsd_simple_type):
    """
    """
    restriction=get_restriction_from_xsd_simple_type(xsd_simple_type)
    return restriction.xpath('./xsd:enumeration/@value',
                             namespaces=ns)

    
    
    
    
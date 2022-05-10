# -*- coding: utf-8 -*-
"""
Created on Mon May  9 12:01:35 2022

@author: cvskf
"""

def nntag(element):
    """Returns the tag without the namespace ('no namespace tag')
    
    Example:
        
    >>> print(gbXML.tag)
    {http://www.gbxml.org/schema}gbXML
    >>> print(gbXML.nntag)
    gbXML
    
    :rtype: str
    
    """
    return element.tag.split('}')[1]


def xsd_type_to_python_type(xsd_type):
    """Returns the python type for a given xsd type.
    
    :param xsd_type: The xsd type to be converted.
    :type xsd_type: str
    
    :raises Exception: If an unrecognized xsd_type is supplied.
    
    :rtype: bol, str, float
    
    """
    if xsd_type=='xsd:boolean':
        return bool
    
    elif xsd_type=='xsd:NMTOKEN':
        return str
    
    elif xsd_type=='xsd:ID':
        return str
    
    elif xsd_type=='xsd:double':
        return float
    
    elif xsd_type=='xsd:string':
        return str
    
    elif xsd_type=='xsd:decimal':
        return float
    
    elif xsd_type=='xsd:IDREF':
        return str
    
    else:
        raise Exception(xsd_type)
    
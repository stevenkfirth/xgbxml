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



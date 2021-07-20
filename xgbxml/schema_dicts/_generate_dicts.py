# -*- coding: utf-8 -*-

"""This module is run as part of the package development, rather than by package users.

It reads the .xsd files, converts them into Python dictionries, and saves the
dictionaries in this directory.

"""
import json
from lxml import etree

ns={'xsd':r'http://www.w3.org/2001/XMLSchema'}


def enumeration_dict(enumeration):
    """
    
    """
    annotations_texts=enumeration.xpath(r'./xsd:annotation/xsd:*/text()',namespaces=ns)
    
    return {'annotations':annotations_texts}
    

def enumerations_dict(enumerations):
    """
    
    """
    return {enumeration.get('value'):enumeration_dict(enumeration)
             for enumeration in enumerations}


def simpleType_dict(simpleType):
    """
    
    """
    annotations_texts=simpleType.xpath(r'./xsd:annotation/xsd:*/text()',namespaces=ns)
    restriction=simpleType.xpath(r'./xsd:restriction',namespaces=ns)[0]
    enumerations=restriction.xpath(r'./xsd:enumeration',namespaces=ns)
    try:
        minInclusive=restriction.xpath(r'./xsd:minInclusive',namespaces=ns)[0]
    except IndexError:
        minInclusive=None
    try:
        maxInclusive=restriction.xpath(r'./xsd:maxInclusive',namespaces=ns)[0]
    except IndexError:
        maxInclusive=None
    d={'annotations':annotations_texts,
       'enumerations':enumerations_dict(enumerations),
       'minInclusive':dict(minInclusive.attrib) if minInclusive is not None else {},
       'maxInclusive':dict(maxInclusive.attrib) if maxInclusive is not None else {},
       'restriction':dict(restriction.attrib)
      }
    return d


def simpleTypes_dict(simpleTypes):
    """
    """
    return {simpleType.get('name'):simpleType_dict(simpleType) 
            for simpleType in simpleTypes}


def attribute_dict(attribute):
    d=dict(attribute.attrib)
    del d['name']
    annotations_texts=attribute.xpath(r'./xsd:annotation/xsd:*/text()',namespaces=ns)
    d['annotations']=annotations_texts
    try:
        simpleType=attribute.xpath(r'./xsd:simpleType',namespaces=ns)[0]
        d.update(simpleType_dict(simpleType))
    except IndexError:
        pass
    return d


def attributes_dict(attributes):
    return {attribute.attrib['name']:attribute_dict(attribute) for attribute in attributes}


def child_element_dict(child_element):
    annotations_texts=child_element.xpath(r'./xsd:annotation/xsd:*/text()',namespaces=ns)
    d=dict(child_element.attrib)
    del d['ref']
    d['annotations']=annotations_texts
    return d


def child_elements_dict(child_elements):
    return {child_element.attrib['ref']:child_element_dict(child_element) for child_element in child_elements}


def element_dict(element):
    annotations_texts=element.xpath(r'./xsd:annotation/xsd:*/text()',namespaces=ns)
    attributes=(element.xpath(r'./xsd:complexType/xsd:attribute',namespaces=ns) or
                element.xpath(r'./xsd:complexType/xsd:simpleContent/xsd:extension/xsd:attribute',namespaces=ns)
               )
    try:
        extension=element.xpath(r'./xsd:complexType/xsd:simpleContent/xsd:extension',namespaces=ns)[0]
    except IndexError:
        extension=None
    try:
        simpleType=element.xpath(r'./xsd:simpleType',namespaces=ns)[0]
    except IndexError:
        simpleType=None
    try:
        choice=element.xpath(r'./xsd:complexType/xsd:choice',namespaces=ns)[0]
        child_elements=choice.xpath(r'./xsd:element',namespaces=ns)
    except IndexError:
        try:
            all_=element.xpath(r'./xsd:complexType/xsd:all',namespaces=ns)[0]
            child_elements=all_.xpath(r'./xsd:element',namespaces=ns)
            choice=None
        except IndexError:
            choice=None
            child_elements=[]
    return {'annotations':annotations_texts,
            'attributes':attributes_dict(attributes),
            'extension':dict(extension.attrib) if extension is not None else {},
            'child_elements':child_elements_dict(child_elements),
            'choice':dict(choice.attrib) if choice is not None else {},
            'simpleType':simpleType_dict(simpleType) if simpleType is not None else {},
            'type':element.get('type')
           }


def elements_dict(elements):
    """
    """
    return {element.attrib['name']:element_dict(element) 
            for element in elements}


def schema_dict(schema):
    """
    """
    annotations_texts=schema.xpath(r'./xsd:annotation/xsd:*/text()',namespaces=ns)
    simpleTypes=schema.xpath(r'./xsd:simpleType',namespaces=ns)
    elements=schema.xpath(r'./xsd:element',namespaces=ns)
    d={'annotations':annotations_texts,
       'simpleTypes':simpleTypes_dict(simpleTypes),
       'elements':elements_dict(elements)}
    d.update(dict(schema.attrib))
    return d
    

def get_schema_dict(version):
    ""
    schema_file=r'../schemas/GreenBuildingXML_Ver%s.xsd' % version
    schema_element_tree = etree.parse(schema_file)
    schema_root=schema_element_tree.getroot()
    d=schema_dict(schema_root)
    return d


# CREATE AND SAVE THE SCHEMA DICTIONARIES 
import os
for fp in os.listdir(r'../schemas'):
    if fp.startswith('__'):continue
    print(fp)
    version=fp[-8:-4]
    #print(version)
    with open('schema_dict_%s.json' % version.replace('.','_'),'w') as f:
        json.dump(get_schema_dict(version), f, indent=4)





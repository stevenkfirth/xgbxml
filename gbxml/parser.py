# -*- coding: utf-8 -*-


import json
import importlib.resources as pkg_resources
import importlib
from . import schema_dicts


from .gbElement import gbElement
#from .gbXML import gbXML
#from .Campus import Campus
#from .Location import Location


from .auto import gbElements_6_01

from lxml import etree


parser = etree.XMLParser()
lookup = etree.ElementNamespaceClassLookup()
parser.set_element_class_lookup(lookup)

ns='http://www.gbxml.org/schema'
namespace = lookup.get_namespace(ns)
namespace[None]=gbElement

version='6.01'
schema_text = pkg_resources.read_text(schema_dicts, 
                                      'schema_dict_%s.json' % version.replace('.','_'))

schema_dict=json.loads(schema_text)

for k,v in gbElements_6_01.__dict__.items():
    
    if not k.startswith('__'):
        
        element_name=k[:-5].replace('-','_')
        #print(element_name)
        
        #module = __import__('.'+element_name, globals(), locals(), [element_name], 0)
        
        try:
        
            module = importlib.import_module('.'+element_name,'gbxml')
            kls=module.__dict__[element_name]
            namespace[element_name]=type(element_name,(gbElement,v,kls),dict(_class_schema_dict=schema_dict))
        
        except ModuleNotFoundError:
        
            namespace[element_name]=type(element_name,(gbElement,v),dict(_class_schema_dict=schema_dict))



# # sets up a lxml.etree parser
# # 'parser' is imported and used in etree.parse to parse gbxml files.
# parser = etree.XMLParser()
# lookup = etree.ElementNamespaceClassLookup()
# parser.set_element_class_lookup(lookup)


# # sets up the lookup namespace, so that the custom gbxml classes are used
# #  for the xml elements in place of the regular lxml classes.
# ns='http://www.gbxml.org/schema'
# namespace = lookup.get_namespace(ns)
# namespace[None]=gbElement

# # loops through all globals and adds any gbElement subclasses to namespace
# for k,v in list(globals().items()):
    
#     try:
    
#         if v.__base__==gbElement:
            
#             namespace[k]=v
        
#     except AttributeError:
        
#         pass
    
# from io import BytesIO
# new_gbXML_string=BytesIO(b"""<?xml version="1.0"?>
# <gbXML version="6.01" xmlns="http://www.gbxml.org/schema">
# </gbXML>""")


def create_gbXML(id_=None,
                 engine=None,
                 temperatureUnit='C',
                 lengthUnit='Meters',
                 areaUnit='SquareMeters',
                 volumeUnit='CubicMeters',
                 useSIUnitsForResults=True,
                 version='6.01',
                 SurfaceReferenceLocation=None
                 ):
    ""
    xml='<gbXML version="%s" xmlns="http://www.gbxml.org/schema"></gbXML>' % version
    root=etree.fromstring(xml,parser)
    
    if not id_ is None: root.id_=id_
    if not engine is None: root.engine=engine
    root.temperatureUnit=temperatureUnit
    root.lengthUnit=lengthUnit
    root.areaUnit=areaUnit
    root.volumeUnit=volumeUnit
    root.useSIUnitsForResults=useSIUnitsForResults
    if not SurfaceReferenceLocation is None: root.SurfaceReferenceLocation=SurfaceReferenceLocation
    
    return root
    
    
    
    
    
    
    
    
    

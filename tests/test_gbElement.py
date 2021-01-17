# -*- coding: utf-8 -*-

import unittest

from gbxml import get_parser
from lxml import etree


class Test_gbElement(unittest.TestCase):
    
    def test___repr__(self):
        ""
        self.assertEqual(str(gbXML),
                         '<gbXML>')
        
        
    def test__schema_attribute_dict(self):
        ""
        self.assertEqual(gbXML._schema_attribute_dict('id'),
                         {'type': 'xsd:ID', 
                          'annotations': []})
        
        
    def test__schema_attribute_enumerations_dict(self):
        ""
        self.assertRaises(KeyError,
                          gbXML._schema_attribute_enumerations_dict,'id')
        self.assertEqual(gbXML._schema_attribute_enumerations_dict('engine'),
                         {'DOE2.1e': {'annotations': []}, 
                          'DOE2.2': {'annotations': []}, 
                          'EnergyPlus': {'annotations': []}})
        self.assertEqual(gbXML._schema_attribute_enumerations_dict('temperatureUnit'),
                         {'C': {'annotations': []},
                          'F': {'annotations': []},
                          'K': {'annotations': []},
                          'R': {'annotations': []}})
        
        
        
    def test__schema_attribute_type(self):
        ""
        self.assertEqual(gbXML._schema_attribute_type('id'),
                         'xsd:ID')
        self.assertEqual(gbXML._schema_attribute_type('engine'),
                         'xsd:NMTOKEN')
        self.assertEqual(gbXML._schema_attribute_type('temperatureUnit'),
                         'temperatureUnitEnum')
        
        
    def test__schema_attribute_use(self):
        ""
        self.assertRaises(KeyError,
                          gbXML._schema_attribute_use,'id')
        self.assertRaises(KeyError,
                          gbXML._schema_attribute_use,'engine')
        self.assertEqual(gbXML._schema_attribute_use('temperatureUnit'),
                         'required')
        
        
    def test__schema_attribute_xsd_type(self):
        ""
        self.assertEqual(gbXML._schema_attribute_xsd_type('id'),
                         'xsd:ID')
        self.assertEqual(gbXML._schema_attribute_xsd_type('engine'),
                         'xsd:NMTOKEN')
        self.assertEqual(gbXML._schema_attribute_xsd_type('temperatureUnit'),
                         'xsd:NMTOKEN')
        
        
    def test__schema_attributes_dict(self):
        ""
        return
        self.assertEqual(gbXML._schema_attributes_dict,
                         {'id': {'type': 'xsd:ID', 
                                 'annotations': []}, 
                          'engine': {'annotations': [], 
                                     'enumerations': {'DOE2.1e': {'annotations': []}, 
                                                      'DOE2.2': {'annotations': []}, 
                                                      'EnergyPlus': {'annotations': []}}, 
                                     'minInclusive': {}, 
                                     'maxInclusive': {}, 
                                     'restriction': {'base': 'xsd:NMTOKEN'}}, 
                          'temperatureUnit': {'type': 'temperatureUnitEnum', 
                                              'use': 'required', 
                                              'annotations': ['This attribute specifies the default temperature unit for the entire gbXML document, wherever the temperatureUnit simple type is used.']}, 
                          'lengthUnit': {'type': 'lengthUnitEnum', 
                                         'use': 'required', 
                                         'annotations': ['This attribute specifies the default length unit for the entire gbXML document, wherever the lengthUnit simple type is used.']}, 
                          'areaUnit': {'type': 'areaUnitEnum', 
                                       'use': 'required', 
                                       'annotations': ['This attribute specifies the default area unit for the entire gbXML document, wherever the areaUnit simple type is used.']}, 
                          'volumeUnit': {'type': 'volumeUnitEnum', 
                                         'use': 'required', 
                                         'annotations': ['This attribute specifies the default volume unit for the entire gbXML document, wherever the volumeUnit simple type is used.']}, 
                          'useSIUnitsForResults': {'type': 'xsd:boolean', 
                                                   'use': 'required', 
                                                   'annotations': ['Results will be given in SI or IP units. True = SI units which is the implied default. If False, results will be in english units.']}, 
                          'version': {'type': 'versionEnum', 
                                      'use': 'required', 
                                      'annotations': []}})
        
        
    def test__schema_element_dict(self):
        ""
        return ## TO DO
        self.assertEqual(gbXML._schema_element_dict,
                        {'annotations': [],
                         'attributes': {'areaUnit': {'annotations': ['This attribute specifies the '
                                                                     'default area unit for the entire '
                                                                     'gbXML document, wherever the '
                                                                     'areaUnit simple type is used.'],
                                                     'type': 'areaUnitEnum',
                                                     'use': 'required'},
                                        'engine': {'annotations': [],
                                                   'enumerations': {'DOE2.1e': {'annotations': []},
                                                                    'DOE2.2': {'annotations': []},
                                                                    'EnergyPlus': {'annotations': []}},
                                                   'maxInclusive': {},
                                                   'minInclusive': {},
                                                   'restriction': {'base': 'xsd:NMTOKEN'}},
                                        'id': {'annotations': [], 'type': 'xsd:ID'},
                                        'lengthUnit': {'annotations': ['This attribute specifies the '
                                                                       'default length unit for the '
                                                                       'entire gbXML document, '
                                                                       'wherever the lengthUnit simple '
                                                                       'type is used.'],
                                                       'type': 'lengthUnitEnum',
                                                       'use': 'required'},
                                        'temperatureUnit': {'annotations': ['This attribute specifies '
                                                                            'the default temperature '
                                                                            'unit for the entire gbXML '
                                                                            'document, wherever the '
                                                                            'temperatureUnit simple '
                                                                            'type is used.'],
                                                            'type': 'temperatureUnitEnum',
                                                            'use': 'required'},
                                        'useSIUnitsForResults': {'annotations': ['Results will be '
                                                                                 'given in SI or IP '
                                                                                 'units. True = SI '
                                                                                 'units which is the '
                                                                                 'implied default. If '
                                                                                 'False, results will '
                                                                                 'be in english '
                                                                                 'units.'],
                                                                 'type': 'xsd:boolean',
                                                                 'use': 'required'},
                                        'version': {'annotations': [],
                                                    'type': 'versionEnum',
                                                    'use': 'required'},
                                        'volumeUnit': {'annotations': ['This attribute specifies the '
                                                                       'default volume unit for the '
                                                                       'entire gbXML document, '
                                                                       'wherever the volumeUnit simple '
                                                                       'type is used.'],
                                                       'type': 'volumeUnitEnum',
                                                       'use': 'required'}},
                         'child_elements': {'AirLoop': {'annotations': [],
                                                        'maxOccurs': 'unbounded',
                                                        'minOccurs': '0'},
                                            'Campus': {'annotations': []},
                                            'Construction': {'annotations': [],
                                                             'maxOccurs': 'unbounded',
                                                             'minOccurs': '0'},
                                            'DaySchedule': {'annotations': [],
                                                            'maxOccurs': 'unbounded',
                                                            'minOccurs': '0'},
                                            'DocumentHistory': {'annotations': [], 'minOccurs': '0'},
                                            'ExtEquip': {'annotations': [],
                                                         'maxOccurs': 'unbounded',
                                                         'minOccurs': '0'},
                                            'HydronicLoop': {'annotations': [],
                                                             'maxOccurs': 'unbounded',
                                                             'minOccurs': '0'},
                                            'IntEquip': {'annotations': [],
                                                         'maxOccurs': 'unbounded',
                                                         'minOccurs': '0'},
                                            'Layer': {'annotations': [],
                                                      'maxOccurs': 'unbounded',
                                                      'minOccurs': '0'},
                                            'LightingControl': {'annotations': [],
                                                                'maxOccurs': 'unbounded',
                                                                'minOccurs': '0'},
                                            'LightingSystem': {'annotations': [],
                                                               'maxOccurs': 'unbounded',
                                                               'minOccurs': '0'},
                                            'Material': {'annotations': [],
                                                         'maxOccurs': 'unbounded',
                                                         'minOccurs': '0'},
                                            'Meter': {'annotations': [],
                                                      'maxOccurs': 'unbounded',
                                                      'minOccurs': '0'},
                                            'Results': {'annotations': [],
                                                        'maxOccurs': 'unbounded',
                                                        'minOccurs': '0'},
                                            'Schedule': {'annotations': [],
                                                         'maxOccurs': 'unbounded',
                                                         'minOccurs': '0'},
                                            'Weather': {'annotations': [],
                                                        'maxOccurs': 'unbounded',
                                                        'minOccurs': '0'},
                                            'WeekSchedule': {'annotations': [],
                                                             'maxOccurs': 'unbounded',
                                                             'minOccurs': '0'},
                                            'WindowType': {'annotations': [],
                                                           'maxOccurs': 'unbounded',
                                                           'minOccurs': '0'},
                                            'Zone': {'annotations': [],
                                                     'maxOccurs': 'unbounded',
                                                     'minOccurs': '0'},
                                            'aecXML': {'annotations': [], 'minOccurs': '0'}},
                         'choice': {'maxOccurs': 'unbounded', 'minOccurs': '0'},
                         'extension': {},
                         'simpleType': {},
                         'type': None}
                        )
        
        
    def test__schema_element_text_xsd_type(self):
        ""
        CADModelAzimuth=gbXML.Campus.Location.CADModelAzimuth
        self.assertEqual(CADModelAzimuth._schema_element_text_xsd_type,
                         'xsd:double')
        StationId=gbXML.Campus.Location.get_children('StationId')[0]
        self.assertEqual(StationId._schema_element_text_xsd_type,
                         'xsd:string')
        
        
    def test__getroot(self):
        ""
        self.assertEqual(gbXML._getroot,
                         gbXML)
        
        
    def test__schema_dict(self):
        ""
        return
        self.assertEqual(list(gbXML._schema_dict.keys()),
                         ['annotations', 
                          'simpleTypes', 
                          'elements', 
                          'targetNamespace', 
                          'elementFormDefault', 
                          'attributeFormDefault', 
                          'version'])
        
        
    def test__ns(self):
        ""
        self.assertEqual(gbXML._ns,
                         {'gbxml':'http://www.gbxml.org/schema'})
        
        
    def test__version(self):
        ""
        self.assertEqual(gbXML._version,
                         '0.37')
        
    
    def test__xsd_type_to_python_type(self):
        ""
        self.assertEqual(gbXML._xsd_type_to_python_type('xsd:boolean'),
                         bool)
        self.assertEqual(gbXML._xsd_type_to_python_type('xsd:NMTOKEN'),
                         str)
        self.assertEqual(gbXML._xsd_type_to_python_type('xsd:ID'),
                         str)
    
    
    def test_attributes(self):
        ""
        self.assertEqual(gbXML.attributes,
                         {'useSIUnitsForResults': False, 
                          'temperatureUnit': 'C', 
                          'lengthUnit': 'Feet', 
                          'areaUnit': 'SquareFeet', 
                          'volumeUnit': 'CubicFeet', 
                          'version': '0.37'})
    
    
    def test_id(self):
        ""
        self.assertEqual(gbXML.Campus.id,
                         'aim0002')
    
    
    def test_get_attribute(self):
        ""
        self.assertEqual(gbXML.get_attribute('useSIUnitsForResults'),
                         False)
        self.assertEqual(gbXML.get_attribute('temperatureUnit'),
                         'C')
   
    
    def test_get_child(self):
        ""
        self.assertEqual(gbXML.get_child('Campus','aim0002').nntag,#
                         'Campus')
        
        
    def test_get_children(self):
        ""
        self.assertEqual(gbXML.get_children('Campus'),
                         [gbXML.get_child('Campus')])
    
    
    def test_set_attribute(self):
        ""
        gbXML.set_attribute('id','id0001')
        self.assertEqual(gbXML.get_attribute('id'),
                         'id0001')
        
        gbXML.set_attribute('useSIUnitsForResults',True)
        self.assertEqual(gbXML.get('useSIUnitsForResults'),
                         'true')
        
        self.assertRaises(KeyError,
                          gbXML.set_attribute,'my_attribute',None)
        
        self.assertRaises(ValueError,
                          gbXML.set_attribute,'temperatureUnit','my_value')
    
    
    def test_nntag(self):
        ""
        self.assertEqual(gbXML.nntag,
                         'gbXML')
        
    
    def test_value(self):
        ""
        self.assertEqual(gbXML.Campus.Location.CADModelAzimuth.value,
                         0)
        self.assertEqual(gbXML.Campus.Location.get_children('StationId')[0].value,
                         '52939_2004')
        
    
    def test_value_setter(self):
        ""
        
    
if __name__=='__main__':
    
    fp=r'files\gbXMLStandard.xml'
    parser=get_parser()
    tree = etree.parse(fp,parser)
    gbXML=tree.getroot()
    unittest.main(Test_gbElement())
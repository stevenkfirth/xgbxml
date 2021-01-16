# -*- coding: utf-8 -*-

#from .gbSchema import schemas_dict

from lxml import etree


class gbElement(etree.ElementBase):
    """The default element class for xml elements in a gbXML file.
    
    """
    
    def __repr__(self):
        ""
        try:
            id_=self.get_attribute('id')
            id_st=' (id="%s")' % id_
        except KeyError:
            id_st=''
        
        
        if self.__class__.__name__=='gbElement':
            return '<%s %s%s>' % (self.__class__.__name__,
                                  self.nntag,
                                  id_st)
        else:
            return '<%s%s>' % (self.__class__.__name__,
                               id_st)
    
    
    def _schema_attribute_dict(self,attribute_name):
        """The schema dictionary of the named attribute.
    
        """
        return self._schema_attributes_dict[attribute_name]
    
    
    def _schema_attribute_enumerations_dict(self,attribute_name):
        """The schema enumerations dictionary of the named attribute
        
        :raises KeyError: If attribute does not have any enumerations
        
        """
        schema_attribute_dict=self._schema_attribute_dict(attribute_name)
        try:
            return schema_attribute_dict['enumerations']
        except KeyError:
            type_=self._schema_attribute_type(attribute_name)
            return self._schema_dict['simpleTypes'][type_]['enumerations']
    
    
    def _schema_attribute_type(self,attribute_name):
        ""
        schema_attribute_dict=self._schema_attribute_dict(attribute_name)
        return (schema_attribute_dict.get('type') or
                schema_attribute_dict['restriction']['base'])
    
    
    def _schema_attribute_use(self,attribute_name):
        "The value of the 'use' schema attribute of the named attribute."
        schema_attribute_dict=self._schema_attribute_dict(attribute_name)
        return schema_attribute_dict['use']
    
    
    def _schema_attribute_xsd_type(self,attribute_name):
        """The xsd type of the named attribute according to the schema.
        
        """
        type_=self._schema_attribute_type(attribute_name)
        if type_.startswith('xsd:'):
            return type_
        else:
            return self._schema_dict['simpleTypes'][type_]['restriction']['base']
    
    
    @property
    def _schema_attributes_dict(self):
        ""
        return self._schema_element_dict['attributes']
    
    
    @property
    def _schema_element_dict(self):
        """The schema dict for the element
        
        """
        return self._schema_dict['elements'][self.nntag]
    
    
    @property
    def _schema_element_text_xsd_type(self):
        ""
        type_=self._schema_element_dict['type']
        if type_ is not None:
            return type_
        else:
            return self._schema_element_dict['extension']['base']
    
    
    @property
    def _getroot(self):
        """The root element of the gbXML file
        
        :rtype: gbXML
        
        """
        return self.getroottree().getroot()
    
    
    @property
    def _schema_dict(self):
        """Returns the schema dict
        
        :rtype: dict
        
        """
        #print(self.__class__)
        return self._class_schema_dict  # a class variable defined in parser.py
    
    
    @property
    def _ns(self):
        "The namespace dictionary for xpath calls"
        return {'gbxml':'http://www.gbxml.org/schema'}
    
    
    @property
    def _version(self):
        """The gbXML version being used
        
        :rtype: str
        
        """
        return self._getroot.attrib['version']
    
    
    def _xsd_type_to_python_type(self,xsd_type):
        ""
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
        
        else:
            raise Exception(xsd_type)
        
        
    @property
    def attributes(self):
        ""
        return {k:self.get_attribute(k) for k in self.attrib}
        
    
    @property
    def id(self):
        ""
        return self.get_attribute('id')
            
    @id.setter
    def id(self,value):
        self.set_attribute('id',value)
        
    
    def add_child(self,child_nntag,**kwargs):
        ""
        self.append(etree.Element('{http://www.gbxml.org/schema}%s' % child_nntag))
        child=self.get_children(child_nntag)[-1]
        for k,v in kwargs.items():
            if v is not None:
                child.set_attribute(k,v)
        return child
        
    
    def get_attribute(self,attribute_name):
        ""
        value=self.attrib[attribute_name]
        xsd_type=self._schema_attribute_xsd_type(attribute_name)
        python_type=self._xsd_type_to_python_type(xsd_type)
        
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
    
    
    def get_child(self,child_nntag,child_id=None):
        ""
        if child_id is None:
            return self.find('gbxml:%s' % child_nntag,namespaces=self._ns)        
        else:
            return self.find(r'./gbxml:%s[@id="%s"]' % (child_nntag,child_id), 
                             namespaces=self._ns)
    
    
    def get_children(self,child_nntag):
        ""
        return self.findall('gbxml:%s' % child_nntag,
                            namespaces=self._ns)
    
    
    def set_attribute(self,attribute_name,value):
        ""
        if not attribute_name in self._schema_attributes_dict:
            raise KeyError('Attribute name "%s" in not in schema' % attribute_name)
        
        try:
            enumerations=self._schema_attribute_enumerations_dict(attribute_name)
            if not value in enumerations:
                raise ValueError('Attribute value "%s" must be one of the enumerations' % value)
        except KeyError:
            pass
        
        xsd_type=self._schema_attribute_xsd_type(attribute_name)
        python_type=self._xsd_type_to_python_type(xsd_type)
        
        if python_type is str:
            
            value2=str(value)
        
        elif python_type is bool:
            
            if value is True:
                value2='true'
            else:
                value2='false'
            
        else:
            
            raise Exception()
            
        self.set(attribute_name,value2)
        
        
    @property
    def nntag(self):
        """Returns the tag without the namespace ('no namespace tag')
        
        """
        return self.tag.split('}')[1]
    
    
    @property
    def value(self):
        ""
        
        xsd_type=self._schema_element_text_xsd_type
        python_type=self._xsd_type_to_python_type(xsd_type)
        
        return python_type(self.text)
    
    
    @value.setter
    def value(self,value):
        ""
        
        
        
        self.text=str(value)
    
    
    
        
    
        
        
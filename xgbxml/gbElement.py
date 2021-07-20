# -*- coding: utf-8 -*-

#from .gbSchema import schemas_dict

from lxml import etree


class gbElement(etree.ElementBase):
    """The default element class for the gbxml parser.
    
    """
    
    def __repr__(self):
        """The rper for the class
        
        :returns: A different value is returned depending on if this is the 
        gbElement class or a subclass, and/or if the element has an 'id' attribute.
        :rtype: str

        """
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
    
        :param attribute_name: The name of the attribute.
        :param attribute_name: str
        
        :rtype: dict
    
        """
        return self._schema_attributes_dict[attribute_name]
    
    
    def _schema_attribute_enumerations_dict(self,attribute_name):
        """The schema enumerations dictionary of the named attribute.
        
        :param attribute_name: The name of the attribute.
        :param attribute_name: str
        
        :raises KeyError: If attribute does not have any enumerations
        
        :rtype: dict
        
        """
        schema_attribute_dict=self._schema_attribute_dict(attribute_name)
        try:
            return schema_attribute_dict['enumerations']
        except KeyError:
            type_=self._schema_attribute_type(attribute_name)
            return self._schema_dict['simpleTypes'][type_]['enumerations']
    
    
    def _schema_attribute_type(self,attribute_name):
        """Returns the attribute type.
        
        :param attribute_name: The name of the attribute.
        :param attribute_name: str
        
        :returns: This can return an xsd type or a simpleType.
        :rtype: str
        
        """
        schema_attribute_dict=self._schema_attribute_dict(attribute_name)
        return (schema_attribute_dict.get('type') or
                schema_attribute_dict['restriction']['base'])
    
    
    def _schema_attribute_use(self,attribute_name):
        """The value of the 'use' schema attribute of the named attribute.
        
        :param attribute_name: The name of the attribute.
        :param attribute_name: str
        
        :rtype: str

        """
        schema_attribute_dict=self._schema_attribute_dict(attribute_name)
        return schema_attribute_dict['use']
    
    
    def _schema_attribute_xsd_type(self,attribute_name):
        """The xsd type of the named attribute according to the schema.
        
        :param attribute_name: The name of the attribute.
        :param attribute_name: str
        
        :rtype: str
        
        """
        type_=self._schema_attribute_type(attribute_name)
        if type_.startswith('xsd:'):
            return type_
        else:
            return self._schema_dict['simpleTypes'][type_]['restriction']['base']
    
    
    @property
    def _schema_attributes_dict(self):
        """Returns the attributes dict of the element.
        
        :rtype: dict
        
        """
        return self._schema_element_dict['attributes']
    
    
    @property
    def _schema_element_dict(self):
        """The schema dict for the element.
        
        :rtype: dict
        
        """
        return self._schema_dict['elements'][self.nntag]
    
    
    @property
    def _schema_element_text_xsd_type(self):
        """The xsd type for the text of the element.
        
        :raises KeyError: If the element does not contain text according to the schema.
        
        :rtype: str
        
        """
        #print(self._schema_element_dict)
        type_=self._schema_element_dict['type']
        if type_ is not None:
            return type_
        else:
            try:
                return self._schema_element_dict['extension']['base']
            except KeyError:
                return self._schema_element_dict['simpleType']['restriction']['base']
    
    @property
    def _getroot(self):
        """The root element of the lxml tree.
        
        :rtype: gbXML
        
        """
        return self.getroottree().getroot()
    
    
    @property
    def _schema_dict(self):
        """Returns the entire json schema dictionary.
        
        ..note::
            
            The json schema dictionary is stored as a class variable, 
            created in the `get_parser` function.
        
        :rtype: dict
        
        """
        return self._class_schema_dict  # a class variable defined in parser.py
    
    
    @property
    def _ns(self):
        """The namespace dictionary for xpath calls.
        
        :rtype: dict
        
        """
        return {'gbxml':'http://www.gbxml.org/schema'}
    
    
    @property
    def _version(self):
        """The gbXML version being used in the lxml tree.
        
        :rtype: str
        
        """
        return self._getroot.attrib['version']
    
    
    def _xsd_type_to_python_type(self,xsd_type):
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
        
        
    def add_child(self,child_nntag,**kwargs):
        """Adds a new child element to the element.
        
        :param child_nntag: The 'no namespace' tag of the child element.
        :type child_nntag: str
        :param kwargs: Attributes to be set for the child element.
        
        :returns: The newly created child element.
        :rtype: (subclass of) gbElement
        
        """
        self.append(etree.Element('{http://www.gbxml.org/schema}%s' % child_nntag))
        child=self.get_children(child_nntag)[-1]
        for k,v in kwargs.items():
            if v is not None:
                child.set_attribute(k,v)
        return child
        
        
    @property
    def attributes(self):
        """The attributes of the element.
        
        :returns: A dictionary of attributes where the attribute values
        have been converted to the correct python types according to the schema.
        
        :rtype: dict
        
        """
        return {k:self.get_attribute(k) for k in self.attrib}
        
    
    def display(self):
        """Displays the xml of the element.
        
        """
        print(etree.tostring(self, pretty_print=True).decode())
    
    
    @property
    def id(self):
        """The id of the element.
        
        :raises KeyError: If, on retrieval, the 'id' attribute is not present in the element.
        
        :rtype: str
        
        """
        return self.get_attribute('id')
            
    
    @id.setter
    def id(self,value):
        ""
        self.set_attribute('id',value)
        
    
    
        
    
    def get_attribute(self,attribute_name):
        """Returns the attribute value as a python type.
        
        :param attribute_name: The name of the attribute.
        :param attribute_name: str
        
        :raises KeyError: If the attribute is not present in the element.
        
        :rtype: bool, str, float
        
        """
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
            
            result=self.find('gbxml:%s' % child_nntag,namespaces=self._ns)        
            if result is None:
                raise KeyError('Child element with nntag "%s" does not exist' % child_nntag)
            else:
                return result
        
        else:
            
            result=self.find(r'./gbxml:%s[@id="%s"]' % (child_nntag,child_id), 
                             namespaces=self._ns)
            if result is None:
                raise KeyError('Child element with nntag "%s" and id "%s" does not exist' % (child_nntag,child_id))
            else:
                return result
        
    
    def get_children(self,child_nntag):
        """Returns child elements with a specified tag.
        
        :param child_nntag: The 'no e coercednamespace' tag of the child elements.
        :type child_nntag: str
        
        :rtype: list ??

        """
        return self.findall('gbxml:%s' % child_nntag,
                            namespaces=self._ns)
    
    
    def set_attribute(self,attribute_name,value):
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
        
        return value2
        
        
    @property
    def nntag(self):
        """Returns the tag without the namespace ('no namespace tag')
        
        Example:
            
        >>> print(gbXML.tag)
        {http://www.gbxml.org/schema}gbXML
        >>> print(gbXML.nntag)
        gbXML
        
        :rtype: str
        
        """
        return self.tag.split('}')[1]
    
    
    @property
    def value(self):
        """The value of the element text as a python type.
        
        :rtype: str, float
        
        """
        xsd_type=self._schema_element_text_xsd_type
        python_type=self._xsd_type_to_python_type(xsd_type)
        
        return python_type(self.text)
    
    
    @value.setter
    def value(self,value):
        ""
        self.text=str(value)
    
    
    
        
    
        
        
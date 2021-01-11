# -*- coding: utf-8 -*-

from lxml import etree


class gbxmlElement(etree.ElementBase):
    ""
    def __repr__(self):
        ""
        return '<%s %s>' % (self.__class__.__name__,
                            self.tag)
    
    
    def test(self):
        ""
        print('YES!')
        
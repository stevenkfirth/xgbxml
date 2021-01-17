# -*- coding: utf-8 -*-

class Campus():
    ""
    
    def get_Space(self,id):
        """Returns a Space element belonging to the Campus.
        
        :raises KeyError: If the space does not exist.
        
        :rtype: Space
        
        """
        try:
            return self.xpath(r'./gbxml:Building/gbxml:Space[@id="%s"]' % (id),
                              namespaces=self._ns)[0]
        except IndexError:
            raise KeyError('Element with id="%s" does not exist in the xml tree.' % id)
    
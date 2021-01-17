# -*- coding: utf-8 -*-

import unittest

from gbxml import create_gbXML


class Test_Campus(unittest.TestCase):
   

    def test_get_Space(self):
        ""
        gbXML=create_gbXML()
        c=gbXML.add_Campus()
        c.add_Building().add_Space(id='space1')
        
        self.assertEqual(c.get_Space(id='space1').id,
                         'space1')


        
if __name__=='__main__':
    
    unittest.main(Test_Campus())
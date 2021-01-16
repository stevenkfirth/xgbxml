# -*- coding: utf-8 -*-

import unittest

from gbxml import schemas_dict
from lxml import etree


class Test_gbSchema(unittest.TestCase):
   
    
    def test_(self):
        ""
        print(list(schemas_dict.keys()))
        
    
if __name__=='__main__':
    
    unittest.main(Test_gbSchema())
    
    
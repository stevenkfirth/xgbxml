# -*- coding: utf-8 -*-

# automatically generates pages and toc

import os
import inspect
import importlib

from xgbxml import custom_bases
from xgbxml.auto import gbElements_6_01
versions=['0_32','0_33','0_34','0_35','0_36','0_37',
          '5_00','5_01','5_10','5_11','5_12',
          '6_01']

def get_gbElements_filenames():
    ""
    return [x[:-3] for x in os.listdir(r'../xgbxml/auto')
            if x.startswith('gbElements')]
        
gbElements_filenames=get_gbElements_filenames()
print(gbElements_filenames)

def import_gbElements_modules():
    ""
    return {x:importlib.import_module('.auto.%s' % x,'xgbxml') 
            for x in gbElements_filenames}

gbElements_modules=import_gbElements_modules()
print(gbElements_modules)

def get_gbElements_class_names(gbElements_module):
    ""
    x=filter(lambda x: not x.startswith('__'),
             gbElements_module.__dict__.keys())
    x=map(lambda x: x[:-5], x)
    return list(x)

print(get_gbElements_class_names(gbElements_modules['gbElements_6_01']))
    
def get_all_gbElements_class_names():
    ""
    result=set()
    for gbElements_module in gbElements_modules.values():
        result.update(get_gbElements_class_names(gbElements_module))
    return result

all_gbElements_class_names=get_all_gbElements_class_names()
print(all_gbElements_class_names)

def get_custom_bases_class_names():
    ""
    x=filter(lambda x: x in all_gbElements_class_names,
             custom_bases.__dict__.keys())
    return list(x)

custom_bases_class_names=get_custom_bases_class_names()
print(custom_bases_class_names)

def create_index_page():
    ""
    with open('index.rst','w') as f:
        f.write("""
Welcome to xgbxml's documentation!
==================================

.. toctree::
   :maxdepth: 2
   :caption: Start Here:
   
   Overview
   get_parser
   create_gbXML
   shared_methods
   
.. toctree::
   :maxdepth: 2
   :caption: Custom Methods by Class:

   %s
   
.. toctree::
   :maxdepth: 2
   :caption: Auto Methods by Version:

   %s
      

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

""" % ('\n   '.join(['auto_custom_class_pages/%s' % x 
                    for x in custom_bases_class_names]),
       '\n   '.join(['auto_auto_methods_pages/%s' % x 
                    for x in gbElements_filenames[::-1]])
       ))

def create_custom_bases_class_pages():
    ""
    for name in custom_bases_class_names:
        with open(os.path.join('auto_custom_class_pages','%s.rst' % name), 'w') as f:
            f.write(name + '\n')
            f.write('='*len(name) + '\n')
            f.write('\n')
            f.write('.. autoclass:: xgbxml.custom_bases.%s\n' % name)
            f.write('   :members:\n')
            f.write('\n')
            
            
def create_auto_methods_pages():
    ""
    for name in gbElements_filenames:
        with open(os.path.join('auto_auto_methods_pages','%s.rst' % name), 'w') as f:
            f.write(name + '\n')
            f.write('='*len(name) + '\n')
            f.write('\n')
            f.write('.. automodule:: xgbxml.auto.%s\n' % (name))
            f.write('   :members:\n')
            f.write('   :undoc-members:\n')
            f.write('\n')
            
        #break
        



create_index_page()
create_custom_bases_class_pages()
#create_auto_methods_pages()

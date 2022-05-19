# -*- coding: utf-8 -*-
"""
Created on Thu May 19 09:37:43 2022

@author: cvskf
"""



import os
import importlib
import inspect

for file in os.listdir():
    print(file)
    if file.startswith('gbElements'):
        
        version_=file[-7:-3]
        print(version_)
        version=version_.replace('_','.')
        print(version)
        
        with open(os.path.join(os.pardir,
                               os.pardir,
                               'docs',
                               'auto_auto_methods_pages',
                               f'{version}_index.rst'),
                  'w') as f:
            
            f.write(f'Schema Version {version}\n')
            f.write('===================\n\n')
            f.write('.. toctree::\n\n')
            
            
            my_module = importlib.import_module(f'xgbxml.auto.gbElements_{version_}')
        
            print(my_module)
            
            for kls_name,kls in inspect.getmembers(my_module, inspect.isclass):
                
                f.write(f'   {version}/{kls_name}\n')
                
                
                continue  # to avoid recreating the large set of files below each time.
                
            
                with open(os.path.join(os.pardir,
                                       os.pardir,
                                       'docs',
                                       'auto_auto_methods_pages',
                                       f'{version}',
                                       f'{kls_name}.rst'),
                          'w') as f1:
                    
                    f1.write(f'{kls_name}\n')
                    x='='*len(kls_name)
                    f1.write(f'{x}\n\n')
                    f1.write(f'.. autoclass:: xgbxml.auto.gbElements_{version_}.{kls_name}\n')
                    f1.write('   :members:\n')
                    f1.write('   :undoc-members:\n\n')
        

    #break
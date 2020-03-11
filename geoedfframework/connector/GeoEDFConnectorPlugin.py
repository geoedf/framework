#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Parent class for all connector plugins; binds attributes to their values
    allows for bindings to be reset and updated to support sets of binding values
    also binds any variables in the attribute values, given binding values for the variables
"""

import re
from os import listdir
from os.path import isfile, join

class GeoEDFConnectorPlugin:

    def __init__(self):

        # for each attribute, maintains a list of other attributes that it depends on
        # for each attribute, also maintain a list of other attributes that depend on it
        self.dependencies = dict()
        self.rev_dependencies = dict()
        self.orig_vals = dict()

        # loop through the attributes of the object, parsing their value to
        # extract dependencies on other variables
        for key in self.provided_params:
            self.orig_vals[key] = getattr(self,key)
            self.add_dependencies(key,getattr(self,key))

        # set this plugin's type based on the name
        self.set_plugin_type()

    # set this plugin's type 
    def set_plugin_type(self,plugin_type):
        self.plugin_type = plugin_type

    def find_vars(self,value):
        if value is not None and isinstance(value,str):
            return re.findall('\%\{(.+?)\}',value)
        else:
            return []

    # resets parameters that have variables in value to their original values
    # this needs to be run first, each time a new variable binding is instantiated
    def reset_bindings(self):
        for key in self.dependencies:
            setattr(self,key,self.orig_vals[key])
        
    # parse the value, adding any variable names to key's dependencies
    def add_dependencies(self,key,value):

        # find parameters mentioned in the value
        key_dependencies = self.find_vars(value)

        if len(key_dependencies) > 0:

            # set dependencies
            self.dependencies[key] = key_dependencies

            # set reverse dependencies
            for dep_key in key_dependencies:
                if dep_key in self.rev_dependencies:
                    self.rev_dependencies[dep_key].append(key)
                else:
                    self.rev_dependencies[dep_key] = [key]

    # list of variables mentioned in plugin's attributes
    def plugin_dependencies(self):
        return list(self.rev_dependencies.keys())

    # instantiate a set of variable bindings, updating values of any dependent attributes
    def bind_vars(self,var_bind_dict):
        # loop over the variables, only considering dependencies for this plugin
        for var in var_bind_dict.keys():
            if var in self.rev_dependencies:
            value = var_bind_dict[var]
            # loop over every attribute that depends on this variable
            for attr_key in self.rev_dependencies[var]:
                # (partially) instantiate the dependent attribute
                dep_val = getattr(self,attr_key)
                needle = '%{{{}}}'.format(var)
                setattr(self,attr_key,dep_val.replace(needle,value))
        
    # sets the target path for this plugin's outputs
    def set_output_path(self,path):
        self.target_path = path

    # collects the outputs of an input plugin so they can be returned to the
    # workflow engine and used in instantiating the next stage
    # a text filepath argument is provided and this file will be filled with
    # the paths of the files acquired by the plugin
    def collect_outputs(self,output_filename):
        # make sure this is an input plugin
        if self.plugin_type == 'Input':
            with open(output_filename,'w') as output_file:
                for f in listdir(self.target_path):
                    if isfile(join(self.target_path,f)):
                        output_file.write(join(self.target_path,f))
        else:
            raise GeoEDFError('collect_outputs needs to be called on an Input plugin')
                        
                        
                
            
            
            

            
             


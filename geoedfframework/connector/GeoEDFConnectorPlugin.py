#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Parent class for all connector plugins; implements the dependency chain for binding 
    all attributes needed to run the plugins
"""

import re
from functools import reduce

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

    def find_dependent_params(self,value):
        if value is not None and isinstance(value,str):
            return re.findall('\%\{(.+?)\}',value)
        else:
            return []

    # resets parameters that have variables in value to their original values
    # this needs to be run first, each time a new variable binding is instantiated
    def reset_bindings(self):
        for key in self.dependencies:
            setattr(self,key,self.orig_vals[key])
        
    # parse the value, adding any parameter names to key's dependencies
    def add_dependencies(self,key,value):

        # find parameters mentioned in the value
        key_dependencies = self.find_dependent_params(value)

        if len(key_dependencies) > 0:

            # set dependencies
            self.dependencies[key] = self.find_dependent_params(value)

            # set reverse dependencies
            for dep_key in key_dependencies:
                if dep_key in self.rev_dependencies:
                    self.rev_dependencies[dep_key].append(key)
                else:
                    self.rev_dependencies[dep_key] = [key]

    # wrapper for setattr that also updates dependencies
    # assume that value does not contain any variables & is fully instantiated
    def set_param(self,key,value):
        setattr(self,key,value)
        if key in self.rev_dependencies:
            for dep_key in self.rev_dependencies[key]:
                # first (partially) instantiate the dependent variable
                dep_val = getattr(self,dep_key)
                needle = '%{{{}}}'.format(key)
                setattr(self,dep_key,dep_val.replace(needle,value))

            
             


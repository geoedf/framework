#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Executor class that will help execute a connector or processor plugin given 
    bindings for the arguments
"""

import geoedfframework as framework
from framework import ConnectorPlugin, ProcessorPlugin

class GeoEDFExecutor():

    # plugin_inst is a YAML encoding of a connector or processor instance
    # plugin_type is one of 'input','filter','output','processor'
    # var_bindings is optional and provides bindings for one or more variables used in 
    # instance bindings

    def __init__(self,plugin_inst,plugin_type,var_bindings=None):
        self.plugin_type = plugin_type
        self.plugin_inst = plugin_inst
        self.var_bindings = var_bindings

        # parse plugin instance to determine plugin name & default instance bindings
        

    """ Repeatedly binds plugin's variables with a binding combination
        from var_bindings and executes the appropriate method depending on 
        the plugin's type. Also collects the return value for the job: set 
        of values in case of filter, list of filenames in case of input plugin or 
        processor.
        Assume that the workflow engine has already made sure that if variables exist, 
        then there is atleast one binding combination available
    """

    def bind_and_execute(self):
        
        # determine package and module name for plugin to be instantiated

        if var_binding is not None: # if variable bindings exist

            for var_binding in self.var_bindings:

                # create a "fully instantiated" binding

                # instantiate plugin

                # execute standard method for this type -- returns results???

        else: # no need to instantiate any variables

            # instantiate plugin

            # execute standard method for this type -- return results??

        # collect results

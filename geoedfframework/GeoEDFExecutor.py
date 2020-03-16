#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Executor class that will help execute a connector or processor plugin given 
    bindings for the arguments
"""
import importlib
import json
from functools import reduce

class GeoEDFExecutor():

    # workflow_fname is the workflow filename
    # workflow_stage is the workflow stage that needs to be executed (uses : separator for plugins in connectors)
    # target_path is provided as input and is where files produced by this plugin need to be saved
    # target_path is created beforehand by the first job in the workflow
    # output_filename is the name of the text file that stores the outputs of this stage for this binding
    # var_bindings is optional and provides bindings for one or more variables; encoded as a JSON string
    # stage_bindings is also optional and provides bindings for any stage references (file outputs of prior stages)
    # assume exactly one set of bindings is provided as input
    def __init__(self,workflow_fname,workflow_stage,target_path,output_filename,var_bindings=None,stage_bindings=None):

        if var_bindings is not None:
            self.var_bindings = json.loads(var_bindings)
        else:
            self.var_bindings = None

        if stage_bindings is not None:
            self.stage_bindings = json.loads(stage_bindings)
        else:
            self.stage_bindings = None

        # parse workflow YAML to extract the desired workflow stage that needs to be
        # executed
        with open(workflow_fname,'r') as workflow_file:
            workflow = yaml.load(workflow_file)
            self.__workflow_dict = workflow

            plugin_instance_def = self.__workflow_dict

            # if connector, workflow stage has both a number and a plugin type,
            # an optional varname may also be present (in case of filter plugins)
            if ':' in workflow_stage:  # then this is a connector
                sub_stages = workflow_stage.split(':')
                # in case of a connector, the plugin type is the first stage identifier
                plugin_type = sub_stages[1]
                for sub_stage in sub_stages:
                    plugin_instance_def = plugin_instance_def[sub_stage]
            # else we are running a processor
            else:
                plugin_type = 'Processor'
                plugin_instance_def = plugin_instance_def[workflow_stage]

        self.plugin_type = plugin_type
        self.plugin_instance_def = plugin_instance_def

        self.output_path = output_path
        self.output_filename = output_filename

    # creates an instance of a connector plugin class
    # uses the plugin type and instance def determined during init
    def build_connector_plugin(self):
        plugin_cname = 'unknown'
        try:
            # get the class name and parameter bindings for the plugin & import it
            (plugin_cname,plugin_inst), = self.plugin_instance_def.items()
        
            # construct module name; needs plugin type to be lowercase
            plugin_mname = 'GeoEDF.connector.%s.%s' % (self.plugin_type.lower(),plugin_cname)

            plugin_module = importlib.import_module(plugin_mname)
            PluginClass = getattr(plugin_module,plugin_cname)

            plugin_obj = PluginClass(**plugin_inst)

            return plugin_obj
        except:
            raise GeoEDFError('Error constructing %s plugin %s' % (self.plugin_type,plugin_cname))

    # creates an instance of a processor plugin class
    # uses the plugin instance def determined during init
    def build_processor_plugin(self):
        plugin_cname = 'unknown'
        try:
            # get the class name and parameter bindings for the plugin & import it
            (plugin_cname,plugin_inst), = self.plugin_instance_def.items()
        
            # construct module name
            plugin_mname = 'GeoEDF.processor.%s' % plugin_cname

            plugin_module = importlib.import_module(plugin_mname)
            PluginClass = getattr(plugin_module,plugin_cname)

            plugin_obj = PluginClass(**plugin_inst)

            return plugin_obj
        except:
            raise GeoEDFError('Error constructing %s plugin %s' % (self.plugin_type,plugin_cname))

    """ Binds plugin's variables and stage references with given binding combination
        and executes the appropriate method depending on the plugin's type. Also collects 
        the return value for the job: set of values in case of filter, list of filenames in 
        case of input plugin or processor.
    """
    def bind_and_execute(self):
        
        # instantiate the plugin to be executed
        if self.plugin_type == 'Processor':
            plugin_obj = self.build_processor_plugin()
        else:
            plugin_obj = self.build_connector_plugin()

        # set the plugin type, output path & output filename
        plugin_obj.set_output_path(self.output_path)
        plugin_obj.set_output_filename(self.output_filename)
        plugin_obj.set_plugin_type(self.plugin_type)

        # some simple validation to ensure bindings are available for every variable and stage referenced

        plugin_var_refs = plugin_obj.find_vars_used()
        plugin_stage_refs = plugin_obj.find_stages_referenced()

        if self.var_bindings is None:
            if len(plugin_var_refs) > 0:
                all_vars_bound = False
        else:
            all_vars_bound = reduce((lambda a,b: a and b), map((lambda var: var in self.var_bindings), plugin_var_refs))

        if self.stage_bindings is None:
            if len(plugin_stage_refs) > 0:
                all_stages_bound = False
        else:
            all_stages_bound = reduce((lambda a,b: a and b), map((lambda var: var in self.stage_bindings), plugin_stage_refs))

        if not all_vars_bound or not all_stages_bound:
            raise GeoEDFError('Not all variables and stages referenced by plugin have a binding')

        # bind variables and stages
        plugin_obj.bind_vars(self.var_bindings)

        plugin_obj.bind_stage_refs(self.stage_bindings)

        # execute standard method for this plugin type
        try:
            if self.plugin_type == 'Input':
                plugin_obj.get()
            elif self.plugin_type == 'Filter':
                plugin_obj.filter()
            elif self.plugin_type == 'Processor':
                plugin_obj.process()
        except:
            raise GeoEDFError('Error executing plugin')

        # collect results; these are saved to standard output file
        # which is returned to workflow engine
        plugin_obj.collect_outputs()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Parent class for all processor plugins; implements some common methods such as 
    creating the target directory to store processor outputs, etc.
"""

import os
import random

from ..helper.GeoEDFError import GeoEDFError

class GeoEDFProcessorPlugin:

    # sets the target path for this plugin's outputs
    def set_output_path(self,path):
        self.target_path = path



            
             


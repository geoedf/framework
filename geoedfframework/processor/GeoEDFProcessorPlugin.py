#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Parent class for all processor plugins; implements some common methods such as 
    creating the target directory to store processor outputs, etc.
"""

import os
import random

from ..helper.GeoEDFError import GeoEDFError

class GeoEDFProcessorPlugin:

    # create the target directory
    def __init__(self):

        # create a target directory to hold results
        if self.destdir is not None:
            self.create_target_directory(self.destdir)
        else:
            self.create_target_directory('/tmp')
        
    # creates the target directory that holds processor results using the provided prefix argument
    # also sets target_path field; used to check whether target directory has been created
    def create_target_directory(self,prefix):
        # check to make sure valid directory prefix has been provided
        if os.path.exists(prefix) and os.path.isdir(prefix):
            # now need to construct subdirectory to hold results
            random.seed()
            self.target_path = '%s/%d' % (prefix,random.randrange(1000))
            # loop until we find an unused random directory name under this prefix path
            while os.path.exists(self.target_path):
                self.target_path = '%s/%d' % (prefix,random.randrange(1000))

            # make the target directory
            os.makedirs(self.target_path)

        else:
            raise GeoEDFError('Invalid target directory prefix provided to processor')


            
             


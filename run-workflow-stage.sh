#!/bin/bash

#arguments:
#workflow_fname: workflow filepath
#workflow_stage: stage to be executed; encoded as : separated list (for connectors)
#plugin_type: type of plugin to be executed; helps with validation of inputs
#target_path: either path where outputs are to be stored or filepath for filter outputs
#plugin_name; this is used to determine the environment to activate (only for connectors)
#var_bindings: JSON string containing one set of variable bindings (only for connectors)
#stage_bindings: JSON string containing one set of bindings for stage references
#overridden_args: comma separated list of args that need to be overridden
#optional list of file paths to input files corresponding to overridden_args

#simple validation on the minimum number of arguments required
if [ "$#" -lt 4 ]; then
   echo "At least four arguments need to be provided"
   exit 1
fi

# if this is a connector plugin, we need to activate the environment first
if [ "$3" == "Input" ] || [ "$3" == "Filter" ]; then
    env="$5"
    source activate $env
    python3 /usr/local/bin/run-connector-plugin "$@"
else # processor
    python3 /usr/local/bin/run-processor-plugin "$@"
fi

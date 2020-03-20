#!/bin/bash

#arguments:
#workflow_fname: workflow filepath
#workflow_stage: stage to be executed; encoded as : separated list
#plugin_type: type of plugin to be executed; helps with validation of inputs
#target_path: either path where outputs are to be stored or filepath for filter outputs
#plugin_name; this is used to determine the environment to activate (in case of connector)
#var_bindings: JSON string containing one set of variable bindings
#stage_bindings: JSON string containing one set of bindings for stage references

#simple validation on the minimum number of arguments required
if [ "$#" -lt 5 ]; then
   echo "At least 5 arguments need to be provided"
   exit 1
fi

# if this is a connector plugin, we need to activate the environment first
if [ "$3" == "Input" ] || [ "$3" == "Filter" ]; then
    env="$5"
    source activate $env
    python3 /usr/local/bin/run-workflow-stage "$@"
else # processor
    python3 /usr/local/bin/run-workflow-stage "$@"
fi

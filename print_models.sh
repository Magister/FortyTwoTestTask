#!/bin/bash

MANAGE="django-admin.py"
SETTINGS="fortytwo_test_task.settings"
LOG=`date +%Y-%m-%d`.dat

export PYTHONPATH=`pwd`
export DJANGO_SETTINGS_MODULE="${SETTINGS}"

# that fancy "x>&x" swap stdout and stderr to make
# it possible to redirect stderr to pipe
"${MANAGE}" print_models 3>&1 1>&2 2>&3 3>&- | tee "${LOG}"

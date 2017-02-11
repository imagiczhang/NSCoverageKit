#!/bin/bash
# This script is used to run llvm-cov to collect coverage data

if [ -d "$1" -a -n "$2" ]
then
    PROJECT_DIR="$1"
    PROJECT_TARGET="$2"
    PROFDATA=$(/usr/bin/find ${PROJECT_DIR} -name Coverage.profdata | head -n 1)
    BINARY=$(/usr/bin/find ${PROJECT_DIR} -path *${PROJECT_TARGET}.app/${PROJECT_TARGET} | head -n 1)
    xcrun llvm-cov show -arch=x86_64 -instr-profile=${PROFDATA} ${BINARY}
else
    echo "invalid argument: Please follow llvm-cov.sh <project_temp_root> <project_target_name>. Usually <project_temp_root> is the Build/Intermediates directory and you can reveal that from xcodebuild build settings."
fi

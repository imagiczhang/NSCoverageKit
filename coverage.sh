#!/bin/bash
./llvm-cov.sh ../Build/Intermediates \"$XCODE_SCHEME\" | ./coverage.py ../ | tee ../reports/coverage.txt
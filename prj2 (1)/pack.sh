#!/bin/bash

rm *.tar.gz
rm -r __pycache__/
rm -r phase1src/__pycache__/
rm -r phase2src/__pycache__/
rm -r phase3src/__pycache__/
tar cvf prj2.tgz *

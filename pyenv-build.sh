#!/bin/bash

echo "Running autobuild.sh "
./autobuild.sh
./configure --prefix=`pyenv prefix`
python setup.py $1

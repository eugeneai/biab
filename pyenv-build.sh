#!/bin/bash

./autobuild.sh
./configure --prefix=`pyenv prefix`
python setup.py $1

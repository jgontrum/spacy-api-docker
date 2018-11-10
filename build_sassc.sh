#!/bin/bash

mkdir -p /tmp/sass
cd /tmp/sass
git clone https://github.com/sass/sassc.git
. sassc/script/bootstrap
make -C sassc -j4
PREFIX="/usr" make -C sassc install
cd 
rm -rf /tmp/sass


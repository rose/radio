#!/bin/bash
cd bootstrap
if [ `which grunt`x = x ]; then
  echo please install grunt with: npm install -g grunt-cli
  exit
else
  if [ ! -d node_modules ]; then
    echo Installing required node modules, if this fails, please cd bootstrap and run npm install manually
    npm install
  fi
  echo Building bootstrap and moving the compiled files into static/bootstrap/
  grunt dist && rm -rf ../static/bootstrap/* && mv dist/* ../static/bootstrap/
fi

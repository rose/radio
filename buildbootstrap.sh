#!/bin/bash
cd bootstrap
grunt dist && rm -rf ../static/bootstrap/* && mv dist/* ../static/bootstrap/

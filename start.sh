#!/usr/bin/env bash

# start the local service mocks
pushd examples
http-server . &
popd

# start pydashie
source ENV/bin/activate
pushd pydashie
python main.py

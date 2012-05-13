#!/bin/bash
  ./src/build_bandit.py \
  && make -C src/pixel_generator \
  && nmlc bandit.nml --nfo=sprites/bandit.nfo \
  && grfcodec -e bandit.grf \
  && mv bandit.grf /Users/andy/Documents/OpenTTD/data

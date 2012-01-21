#!/usr/bin/env python

source = open('paste_here.txt').read().split('/*-split here-*/')

all_trucks = open('sprites/nml/all_trucks.gnml','w')
all_trucks.write(source[0])
all_trucks.close()

local_strings = open('lang/english.lng.in').read()
lang = open('lang/english.lng', 'w')
lang.write(local_strings + source[1])
lang.close()
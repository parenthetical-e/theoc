SHELL=/bin/bash -O expand_aliases
# DATA_PATH=/Users/qualia/Code/infomercial/data

# Variation of exp57, but the low part of PAC
# (OZ) is done with osc not the pac pop firing
exp1:
	-mkdir data/exp1
	-rm data/exp1/*
	nice -19 python theoc/exp/exp1.py data/exp1/
	
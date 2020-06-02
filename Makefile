SHELL=/bin/bash -O expand_aliases
# DATA_PATH=/Users/qualia/Code/infomercial/data

# ---------------------------------------------------------------------
# 6-1-2020
# c5697a29145eb0ffd544fbda0c7fcc855ee6f5c2
#
# Try out pop, q, and stim rates.
# f = 6, osc_rate = 2 
exp1:
	-mkdir data/exp1
	-rm data/exp1/*
	nice -19 python theoc/exp/exp1.py data/exp1/

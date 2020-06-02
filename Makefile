SHELL=/bin/bash -O expand_aliases
# DATA_PATH=/Users/qualia/Code/infomercial/data

# Try out pop, q, and stim rates.
# f = 6, osc_rate = 2 
exp1:
	-mkdir data/exp1
	-rm data/exp1/*
	nice -19 python theoc/exp/exp1.py data/exp1/

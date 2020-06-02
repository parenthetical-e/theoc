SHELL=/bin/bash -O expand_aliases
# DATA_PATH=/Users/qualia/Code/infomercial/data

# ---------------------------------------------------------------------
# 6-1-2020
# c5697a29145eb0ffd544fbda0c7fcc855ee6f5c2
#
# Sweep num_pop, stim_rate, q, for 20 different stim/trials.
#
# Let's get the lay of this new land. Should be the same as 
# in pacological. I hope. Changing the way I do MI should 
# not have mattered but of course we shall see...
exp1:
	-mkdir data/exp1
	-rm data/exp1/*
	parallel -j 4 -v \
			--joblog 'data/exp1.log' \
			--nice 19 --colsep ',' \
			'python theoc/run_exp.py data/exp1/stim_rate{1}_g{2}_num_pop{4}_q{3} --num_trials=20 --num_background=5 --t=5 --osc_rate=2 --f=6 --g={2} --g_max=8 --q={3} --stim_rate={1} --frac_std=0.01 --m=8 --priv_std=0 --num_pop={4} --stim_seed={5}' ::: 2 6 10 14 18 22 26 30 ::: 1 2 3 4 5 7 8 ::: 0.0 0.5 1.0 ::: 10 25 50 75 100 500 ::: {1..20}

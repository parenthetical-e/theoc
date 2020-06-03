SHELL=/bin/bash -O expand_aliases
# DATA_PATH=/Users/qualia/Code/infomercial/data

# ---------------------------------------------------------------------
# 6-1-2020
# A quick testing exp. 
exp0:
	-mkdir data/exp0
	-rm data/exp0/*
	parallel -j 4 -v \
			--joblog 'data/exp0.log' \
			--nice 19 --colsep ',' \
			'python theoc/run_oc.py data/exp0/stim_rate{1}_g{2}_num_pop{4}_q{3} --num_trials=20 --num_background=5 --t=5 --osc_rate=2 --f=6 --g={2} --g_max=8 --q={3} --stim_rate={1} --frac_std=0.01 --m=60 --num_pop={4}' ::: 30 ::: 1 4 8 ::: 0.0 0.5 1.0 ::: 10 50 100

			
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
			'python theoc/run_oc.py data/exp1/stim_rate{1}_g{2}_num_pop{4}_q{3} --num_trials=20 --num_background=5 --t=5 --osc_rate=2 --f=6 --g={2} --g_max=8 --q={3} --stim_rate={1} --frac_std=0.01 --m={1} --num_pop={4}' ::: 5 10 15 20 25 30 ::: 1 2 3 4 5 7 8 ::: 0.0 0.25 0.5 0.75 1.0 ::: 10 25 50 75 100 500 

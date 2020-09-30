SHELL=/bin/bash -O expand_aliases
# DATA_PATH=/Users/qualia/Code/infomercial/data

# ---------------------------------------------------------------------
# 6-3-2020
# Generates and saves a single example oc simulation. These are the 
# basis for Fig 2 (?) in the final paper.
examples:
	jupyter nbconvert --execute notebooks/examples.ipynb


# ---------------------------------------------------------------------
# 6-1-2020
# A quick testing exp. 
exp0:
	-mkdir data/exp0
	-rm data/exp0/*
	parallel -j 4 -v \
			--joblog 'data/exp0.log' \
			--nice 19 --colsep ',' \
			'python theoc/run_oc.py data/exp0/stim_rate{1}_g{2}_num_pop{4}_q{3} --num_trials=20 --num_background=5 --t=5 --osc_rate=2 --f=6 --g={2} --g_max=8 --q={3} --stim_rate={1} --frac_std=0.01 --m=20 --num_pop={4}' ::: 30 ::: 1 4 8 ::: 0.0 0.5 1.0 ::: 10 50 100

# ---------------------------------------------------------------------
# 6-3-2020
# ba9f3a887843d213ac8d34f25b8ffa4630c8b920
#
# Sweep num_pop, stim_rate, q, for 20 different stim/trials.
#
# Let's get the lay of this new land. Should be the same as 
# in pacological. I hope. Changing the way I do MI should 
# not have mattered but of course we shall see...
#
# RESULT: everything consistent w/ poclogical results (exp70) which were
# in the last paper draft. Some difference with, E. This current version
# makes more sense. And not less. 
#
# This is a good base for Fig 1 results.
exp1:
	-mkdir data/exp1
	-rm data/exp1/*
	parallel -j 4 -v \
			--joblog 'data/exp1.log' \
			--nice 19 --colsep ',' \
			'python theoc/run_oc.py data/exp1/stim_rate{1}_g{2}_num_pop{4}_q{3} --num_trials=20 --num_background=5 --t=5 --osc_rate=2 --f=6 --g={2} --g_max=8 --q={3} --stim_rate={1} --frac_std=0.01 --m={1} --num_pop={4}' ::: 5 10 15 20 25 30 ::: 1 2 3 4 5 7 8 ::: 0.0 0.25 0.5 0.75 1.0 ::: 10 25 50 75 100 500 

# --------------------------------------------------------------------------
# 6/3/2020
# ba9f3a887843d213ac8d34f25b8ffa4630c8b920
#
# Control experiments. 
#
# Fixed most params: 
# -num_pop=50
# -stim_rate=20
# -g=4 (unless noted)
#
# The search: freq, osc_rate, m, num_background
#
# RESULT: None of the controls changed the qual. results. This is as it 
#         should be in linear/rate model.
#
# freq
exp2:
	-mkdir data/exp2
	-rm data/exp2/*
	parallel -j 4 -v \
			--joblog 'data/exp2.log' \
			--nice 19 --colsep ',' \
			'python theoc/run_oc.py data/exp2/f{1} --num_trials=20 --num_background=5 --t=5 --osc_rate=2 --f={1} --g=4 --g_max=8 --q=0.5 --stim_rate=20 --frac_std=0.01 --m=20 --num_pop=50' ::: 4 6 8 12 20 30

# osc_rate (fix g=1, freq=6)
exp3:
	-mkdir data/exp3
	-rm data/exp3/*
	parallel -j 4 -v \
			--joblog 'data/exp3.log' \
			--nice 19 --colsep ',' \
			'python theoc/run_oc.py data/exp3/osc_rate{1} --num_trials=20 --num_background=5 --t=5 --osc_rate={1} --f=6 --g=1 --g_max=8 --q=0.5 --stim_rate=20 --frac_std=0.01 --m=20 --num_pop=50' ::: 2 3 4 6 8

# m (2*stim, 1/2stim)
exp4:
	-mkdir data/exp4
	-rm data/exp4/*
	parallel -j 4 -v \
			--joblog 'data/exp4.log' \
			--nice 19 --colsep ',' \
			'python theoc/run_oc.py data/exp4/m{1} --num_trials=20 --num_background=5 --t=5 --osc_rate=2 --f=6 --g=4 --g_max=8 --q=0.5 --stim_rate=20 --frac_std=0.01 --m={1} --num_pop=50' ::: 10 20 40

# num_background
exp5:
	-mkdir data/exp5
	-rm data/exp5/*
	parallel -j 4 -v \
			--joblog 'data/exp5.log' \
			--nice 19 --colsep ',' \
			'python theoc/run_oc.py data/exp5/num_background{1} --num_trials=20 --num_background={1} --t=5 --osc_rate=2 --f=6 --g=4 --g_max=8 --q=0.5 --stim_rate=20 --frac_std=0.01 --m=20 --num_pop=50' ::: 5 10 15 20 25

# --------------------------------------------------------------------------
# Explore num_pop by log (this might make a nice figure?)
exp6:
	-mkdir data/exp6
	-rm data/exp6/*
	parallel -j 4 -v \
			--joblog 'data/exp6.log' \
			--nice 19 --colsep ',' \
			'python theoc/run_oc.py data/exp6/num_pop{1} --num_trials=20 --num_background=5 --t=5 --osc_rate=2 --f=6 --g=4 --g_max=8 --q=0.5 --stim_rate=20 --frac_std=0.01 --m=20 --num_pop={1}' ::: 10 20 40 80 160 320 640 1280


# -------------------------------------------------------------------------
# 6-8-2020
# fcfbdf34ed6d4555589ec5b9a1202368729afeb2
# 
# Often the ditributions in H calculations have empty bins. This varies by
# cond and so H is biased upwards. I change discrete_entropy to norm by
# Max by default.
# 
# ALSO...
#
# In analyzing PAC on 6/7 I realized I should also be analyzing peak power. 
#
# I modified oc to extract that. Here we rerun exp1, less the pop_size search to adds powers to the results. pop_size is explored on its own in a control, 
# exp6.
# 
# For consistency sake, this should be the new default run for Figure 2,
# or whatever number the main results figure ends up as.
# 
# ALSO...
# 
# The min q isnot 0.05 and not 0 which was causing problems.
exp7:
	-mkdir data/exp7
	-rm data/exp7/*
	parallel -j 4 -v \
			--joblog 'data/exp7.log' \
			--nice 19 --colsep ',' \
			'python theoc/run_oc.py data/exp7/stim_rate{1}_g{2}_num_pop{4}_q{3} --num_trials=20 --num_background=5 --t=5 --osc_rate=2 --f=6 --g={2} --g_max=8 --q={3} --stim_rate={1} --frac_std=0.01 --m={1} --num_pop={4}' ::: 5 10 15 20 25 30 ::: 1 2 3 4 5 7 8 ::: 0.05 0.25 0.5 0.75 1.0 ::: 50 

# -------------------------------------------------------------------------
# 6-8-2020
# fcfbdf34ed6d4555589ec5b9a1202368729afeb2
# Repeat of exp7, but with an increase in trial number to 100. I need more
# density for the power/pac trends. Bigger N is better.
#
# num_trials=100 up from num_trials=20
exp8:
	-mkdir data/exp8
	-rm data/exp8/*
	parallel -j 4 -v \
			--joblog 'data/exp8.log' \
			--nice 19 --colsep ',' \
			'python theoc/run_oc.py data/exp8/stim_rate{1}_g{2}_num_pop{4}_q{3} --num_trials=100 --num_background=5 --t=5 --osc_rate=2 --f=6 --g={2} --g_max=8 --q={3} --stim_rate={1} --frac_std=0.01 --m={1} --num_pop={4}' ::: 5 10 15 20 25 30 ::: 1 2 3 4 5 7 8 ::: 0.05 0.25 0.5 0.75 1.0 ::: 50 


# --------------------------------------------------------------------------
# 6/3/2020
# ba9f3a887843d213ac8d34f25b8ffa4630c8b920
#
# RERUN -  Control experiments. (These were exp2-5). 
#
#				***I changed how H is calculated***
#
# freq
exp9:
	-mkdir data/exp9
	-rm data/exp9/*
	parallel -j 4 -v \
			--joblog 'data/exp9.log' \
			--nice 19 --colsep ',' \
			'python theoc/run_oc.py data/exp9/f{1} --num_trials=20 --num_background=5 --t=5 --osc_rate=2 --f={1} --g=4 --g_max=8 --q=0.5 --stim_rate=10 --frac_std=0.01 --m=10 --num_pop=50' ::: 4 6 8 12 20 30

# osc_rate (fix g=1, freq=6)
exp10:
	-mkdir data/exp10
	-rm data/exp10/*
	parallel -j 4 -v \
			--joblog 'data/exp10.log' \
			--nice 19 --colsep ',' \
			'python theoc/run_oc.py data/exp10/osc_rate{1} --num_trials=20 --num_background=5 --t=5 --osc_rate={1} --f=6 --g=1 --g_max=8 --q=0.5 --stim_rate=10 --frac_std=0.01 --m=10 --num_pop=50' ::: 2 3 4 6 8

# m (2*stim, 1/2stim)
exp11:
	-mkdir data/exp11
	-rm data/exp11/*
	parallel -j 4 -v \
			--joblog 'data/exp11.log' \
			--nice 19 --colsep ',' \
			'python theoc/run_oc.py data/exp11/m{1} --num_trials=20 --num_background=5 --t=5 --osc_rate=2 --f=6 --g=4 --g_max=8 --q=0.5 --stim_rate=10 --frac_std=0.01 --m={1} --num_pop=50' ::: 5 10 20

# num_background
exp12:
	-mkdir data/exp12
	-rm data/exp12/*
	parallel -j 4 -v \
			--joblog 'data/exp12.log' \
			--nice 19 --colsep ',' \
			'python theoc/run_oc.py data/exp12/num_background{1} --num_trials=20 --num_background={1} --t=5 --osc_rate=2 --f=6 --g=4 --g_max=8 --q=0.5 --stim_rate=10 --frac_std=0.01 --m=10 --num_pop=50' ::: 5 10 15 20 25


# --------------------------------------------------------------------------
# 6/9/2020
# c8edc39e9fd734308f34e523d91b413ede922f0b
#
# The div_sub implementation was donw in way the order of div>sub or sub> div
# effected the result. This is inconsistent w/ its basis: 
#
# " Divisive gain modulation enables flexible and rapid entrainment in a 
# neocortical microcircuit model" Papasavvas et al, J neurophys 2020.
exp13:
	-mkdir data/exp13
	-rm data/exp13/*
	parallel -j 2 -v \
			--joblog 'data/exp13.log' \
			--nice 19 --colsep ',' \
			'python theoc/run_oc.py data/exp13/stim_rate{1}_g{2}_num_pop{4}_q{3} --num_trials=100 --num_background=5 --t=5 --osc_rate=2 --f=6 --g={2} --g_max=8 --q={3} --stim_rate={1} --frac_std=0.01 --m={1} --num_pop={4}' ::: 5 10 15 20 25 30 ::: 1 2 3 4 5 7 8 ::: 0.05 0.25 0.5 0.75 0.95 ::: 50 

# --------------------------------------------------------------------------
# 6/12/2020
# 
# Experiment with tonic modulation. Replace oscillation with constant levels of effect.
exp14:
	-mkdir data/exp14
	-rm data/exp14/*
	parallel -j 4 -v \
			--joblog 'data/exp14.log' \
			--nice 19 --colsep ',' \
			'python theoc/run_oc.py data/exp14/stim_rate{1}_g{2}_num_pop{4}_q{3} --num_trials=100 --num_background=5 --t=5 --osc_rate=2 --f=6 --g={2} --g_max=8 --q={3} --stim_rate={1} --frac_std=0.01 --m={1} --num_pop={4} --squelch=True' ::: 5 10 15 20 25 30 ::: 1 2 3 4 5 7 8 ::: 0.05 0.25 0.5 0.75 0.95 ::: 50 

# -------------------------------------------------------------------------
# 9-30-2020
# fcfbdf34ed6d4555589ec5b9a1202368729afeb2
# Repeat of exp6, exploring g as well

exp15:
	-mkdir data/exp15
	-rm data/exp15/*
	parallel -j 4 -v \
			--joblog 'data/exp15.log' \
			--nice 19 --colsep ',' \
			--progress \
			'python theoc/run_oc.py data/exp15/stim_rate{1}_g{2}_num_pop{4}_q{3} --num_trials=100 --num_background=5 --t=5 --osc_rate=2 --f=6 --g={2} --g_max=8 --q={3} --stim_rate={1} --frac_std=0.01 --m={1} --num_pop={4}' ::: 10 ::: 1 2 3 4 5 7 8 ::: 0.5 ::: 10 20 40 80 160 320 640 1280

# 9-30-2020
# fcfbdf34ed6d4555589ec5b9a1202368729afeb2
# Vary osc_rate and g
exp16:
	-mkdir data/exp16
	-rm data/exp16/*
	parallel -j 4 -v \
			--joblog 'data/exp16.log' \
			--nice 19 --colsep ',' \
			--progress \
			'python theoc/run_oc.py data/exp16/stim_rate{1}_g{2}_num_pop{4}_q{3}_osc_rate{5} --num_trials=100 --num_background=5 --t=5 --osc_rate={5} --f=6 --g={2} --g_max=8 --q={3} --stim_rate={1} --frac_std=0.01 --m={1} --num_pop={4}' ::: 10 ::: 1 2 3 4 5 7 8 ::: 0.5 ::: 40 ::: 2 4 6 8 10 12

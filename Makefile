SHELL=/bin/bash -O expand_aliases
# DATA_PATH=/Users/qualia/Code/infomercial/data

# ---------------------------------------------------------------------
# 6-1-2020
# c5697a29145eb0ffd544fbda0c7fcc855ee6f5c2
#

# stim_rates = [2, 6, 10, 14, 18, 22, 26, 30]
# gs = [1, 2, 3, 4, 5, 7, 8]
# qs = [0.0, 0.5, 1.0]
# num_pops = [10, 25, 50, 75, 100, 500]

# num_trials = len(stim_rates) * len(gs) * len(qs) * len(num_pops)
# print(f">>> Starting exp1 - {num_trials} trials")

# # --- Fixed params ----------------------------------------------------
# n_trials = 20
# n_jobs = 4  # Num jobs in parallel
# osc_rate = 2  # Osc. firing rate

# m = 6  # Quantization levels
# t = 5  # Run time
# dt = 0.001  # Sample rate
# f = 6  # Osc frequncy
# g_max = max(gs)  # Max gain
# q = 0.5  # Fraction divisive I
# num_background = 5  # Fix background

# exp1:
# 	-mkdir data/exp1
# 	-rm data/exp1/*
# 	nice -19 python theoc/exp/run_exp.py data/exp1/

# stim_rate-2_g-1_num_pop-25_q-0.0_H
exp1:
	-mkdir data/exp1
	-rm data/exp1/*
	parallel -j 4 -v \
			--joblog 'data/exp1.log' \
			--nice 19 --colsep ',' \
			'python theoc/run_exp.py data/exp1/stim_rate-_{1}_g-{2}1_num_pop-{4}_q-{3} --num_trials=20 --num_background=5 --t=5 --osc_rate=2 --f=6 --g={2} --g_max=8 --q={3} --stim_rate={1} --frac_std=0.01 --m=8 --priv_std=0 --num_pop={4} --stim_seed={5}' ::: 2 6 10 14 18 22 26 30 ::: 1 2 3 4 5 7 8 ::: 0.0 0.5 1.0 ::: 10 25 50 75 100 500 ::: {1..20}

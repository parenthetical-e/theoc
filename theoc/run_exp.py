#! /usr/bin/env python
# -*- coding: utf-8 -*-

import fire
import sys
import pandas as pd
import os
import numpy as np

from joblib import Parallel, delayed
from itertools import product
from collections import defaultdict

from theoc.oc import oscillatory_coupling


def main(name, num_trials=20, verbose=False, **oc_kwargs):
    """Run several OC experiments, saving select results to disk"""

    # -- Init
    # Create basename for the data
    if verbose: print(f">>> Running: {name}")

    # Output structures
    d_H = defaultdict(list)
    d_MI = defaultdict(list)
    d_PAC = defaultdict(list)
    d_rate = defaultdict(list)
    d_dist = defaultdict(list)

    # -- Run
    iterations = range(num_trials)
    for _ in iterations:
        res = oscillatory_coupling(**oc_kwargs)

        # Save parts of the result
        for b in res['H'].keys():
            d_H[b].append(res["H"][b])
        for b in res['MI'].keys():
            d_MI[b].append(res['MI'][b])
        for b in res['PAC'].keys():
            d_PAC[b].append(res['PAC'][b])
        for b in res['dist'].keys():
            d_dist[b].extend(res['dist'][b])
        d_dist["m"].extend(range(1, oc_kwargs["m"] + 1))
        for b in res['spikes'].keys():
            mrate = np.mean(res['spikes'][b].sum(0) / float(oc_kwargs["t"]))
            d_rate[b].append(mrate)

    # -- To disk!
    df_H = pd.DataFrame(d_H)
    df_H.to_csv(name + "_H.csv", index=False)
    df_MI = pd.DataFrame(d_MI)
    df_MI.to_csv(name + "_MI.csv", index=False)
    df_PAC = pd.DataFrame(d_PAC)
    df_PAC.to_csv(name + "_PAC.csv", index=False)
    df_rate = pd.DataFrame(d_rate)
    df_rate.to_csv(name + "_rate.csv", index=False)
    df_dist = pd.DataFrame(d_dist)
    df_dist.to_csv(name + "_dist.csv", index=False)

    return None


if __name__ == "__main__":
    fire.Fire(main)

    # path = sys.argv[1]

    # # --- Experimental params ---------------------------------------------
    # stim_rates = [2, 6, 10, 14, 18, 22, 26, 30]
    # gs = [1, 2, 3, 4, 5, 7, 8]
    # qs = [0.0, 0.5, 1.0]
    # num_pops = [10, 25, 50, 75, 100, 500]

    # num_trials = len(stim_rates) * len(gs) * len(qs) * len(num_pops)
    # print(f">>> Starting exp1 - {num_trials} trials")

    # # --- Fixed params ----------------------------------------------------
    # num_trials = 20
    # n_jobs = 4  # Num jobs in parallel
    # osc_rate = 2  # Osc. firing rate

    # m = 6  # Quantization levels
    # t = 5  # Run time
    # dt = 0.001  # Sample rate
    # f = 6  # Osc frequncy
    # g_max = max(gs)  # Max gain
    # q = 0.5  # Fraction divisive I
    # num_background = 5  # Fix background

    # # -- Run -------------------------------------------------------------
    # params = product(stim_rates, gs, num_pops, qs)

    # Parallel(n_jobs=n_jobs)(delayed(exp)(n, stim_rate, g, num_pop, q)
    #                         for n, (stim_rate, g, num_pop,
    #                                 q) in enumerate(params))
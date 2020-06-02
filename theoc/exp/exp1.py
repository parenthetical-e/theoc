#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pandas as pd
import os
import numpy as np

from joblib import Parallel, delayed
from itertools import product
from collections import defaultdict

from theoc.oc import run


def exp(num_exp, stim_rate, g, num_pop, q):
    # -- Init
    # Drives and iteration counter
    stim_std = .01 * stim_rate

    # Create basename for the data
    basename = f"stim_rate-{stim_rate}_g-{q}_num_pop-{num_pop}_q-{q}"
    print(f">>> Running {num_exp}: {basename}")

    # path the name
    basepath = os.path.join(path, basename)

    # Output structures
    d_H = defaultdict(list)
    d_MI = defaultdict(list)
    d_PAC = defaultdict(list)
    d_rate = defaultdict(list)

    # -- Run
    iterations = range(n_trials)
    for i in iterations:
        res = run(num_pop=num_pop,
                  num_background=num_background,
                  t=t,
                  osc_rate=osc_rate,
                  f=f,
                  g=g,
                  g_max=g_max,
                  q=q,
                  stim_rate=stim_rate,
                  stim_std=stim_std,
                  priv_std=-0,
                  dt=dt,
                  stim_seed=i,
                  seed=None)

        # Save parts of the result
        for b in res['H'].keys():
            d_H[b].append(res["H"][b])
        for b in res['MI'].keys():
            d_MI[b].append(res['MI'][b])
        for b in res['PAC'].keys():
            d_PAC[b].append(res['PAC'][b])
        for b in res['spikes'].keys():
            mrate = np.mean(res['spikes'][b].sum(0) / float(t))
            d_rate[b].append(mrate)

    # -- To disk!
    df_H = pd.DataFrame(d_H)
    df_H.to_csv(basepath + "_H.csv", index=False)
    df_MI = pd.DataFrame(d_MI)
    df_MI.to_csv(basepath + "_MI.csv", index=False)
    df_PAC = pd.DataFrame(d_PAC)
    df_PAC.to_csv(basepath + "_PAC.csv", index=False)
    df_rate = pd.DataFrame(d_rate)
    df_rate.to_csv(basepath + "_rate.csv", index=False)

    return None


if __name__ == "__main__":
    path = sys.argv[1]

    # --- Experimental params ---------------------------------------------
    stim_rates = [2, 6, 10, 14, 18, 22, 26, 30]
    gs = [1, 2, 3, 4, 5, 7, 8]
    qs = [0.0, 0.5, 1.0]
    num_pops = [10, 25, 50, 75, 100, 500]

    num_trials = len(stim_rates) * len(gs) * len(qs) * len(num_pops)
    print(f">>> Starting exp1 - {num_trials} trials")

    # --- Fixed params ----------------------------------------------------
    n_trials = 20
    n_jobs = 4  # Num jobs in parallel
    osc_rate = 2  # Osc. firing rate

    m = 6  # Quantization levels
    t = 5  # Run time
    dt = 0.001  # Sample rate
    f = 6  # Osc frequncy
    g_max = max(gs)  # Max gain
    q = 0.5  # Fraction divisive I
    num_background = 5  # Fix background

    # -- Run -------------------------------------------------------------
    params = product(stim_rates, gs, num_pops, qs)

    Parallel(n_jobs=n_jobs)(delayed(exp)(n, stim_rate, g, num_pop, q)
                            for n, (stim_rate, g, num_pop,
                                    q) in enumerate(params))

#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pandas as pd
import os
import numpy as np
import pyentropy as en
from fakespikes import neurons, rates

# from pacpy.pac import plv as pacfn
from pacpy.pac import ozkurt as pacfn
from joblib import Parallel, delayed
from itertools import product
from collections import defaultdict

from theoc.oc import run


def exp(Istim, g, N, pn):
    # -- Init
    d_H = defaultdict(list)
    d_MI = defaultdict(list)
    d_PAC = defaultdict(list)
    d_rate = defaultdict(list)

    # -- Run
    iterations = range(n_trials)
    for i in iterations:
        print(i)
        res = run(n,
                  n_b,
                  t,
                  Iosc,
                  f,
                  g,
                  g_max,
                  q
                  Istim,
                  Sstim,
                  Ipri,
                  dt,
                  back_type,
                  stim_seed=i)

        # Process the result
        hys = {}
        for b in res['H'].keys():
            hys[b] = res['H'][b]['HY']
        for b in hys.keys():
            d_H[b].append(hys[b])
        for b in res['MI'].keys():
            d_MI[b].append(res['MI'][b])
        for b in res['PAC'].keys():
            d_PAC[b].append(res['PAC'][b])

        for b in res['spikes'].keys():
            mrate = np.mean(res['spikes'][b].sum(0) / float(t))
            d_rate[b].append(mrate)

    # -- Save
    # H
    df_H = pd.DataFrame(d_H)
    df_H.to_csv(basepath + "_H.csv", index=False)

    sum_H = df_H.describe(percentiles=[.05, .25, .75, .95]).T
    sum_H.to_csv(basepath + "_H_summary.csv")

    # MI
    df_MI = pd.DataFrame(d_MI)
    df_MI.to_csv(basepath + "_MI.csv", index=False)

    sum_MI = df_MI.describe(percentiles=[.05, .25, .75, .95]).T
    sum_MI.to_csv(basepath + "_MI_summary.csv")

    # PAC
    df_PAC = pd.DataFrame(d_PAC)
    df_PAC.to_csv(basepath + "_PAC.csv", index=False)

    sum_PAC = df_PAC.describe(percentiles=[.05, .25, .75, .95]).T
    sum_PAC.to_csv(basepath + "_PAC_summary.csv")

    # rate
    df_rate = pd.DataFrame(d_rate)
    df_rate.to_csv(basepath + "_rate.csv", index=False)

    sum_rate = df_rate.describe(percentiles=[.05, .25, .75, .95]).T
    sum_rate.to_csv(basepath + "_rate_summary.csv")


if __name__ == "__main__":
    path = sys.argv[1]

    # --- Experimental params ---------------------------------------------
    Istims = range(2, 32, 4)
    gs = range(1, 9)
    Ns = range(100, 600, 100)
    pns = [0.25, 0.5, 0.75, 1]
    params = product(Istims, gs, Ns, pns)

    # --- Fixed params ----------------------------------------------------
    n_trials = 20
    n_jobs = 12 
    t = 5
    dt = 0.001
    f = 6
    g_max = max(gs)
    q = 0.5
    # back_type = 'constant'
    back_type = 'stim'

    # Drives and iteration counter
    Iosc = 2
    Ipri = 0
    # Iback = 2
    # Ipub = 1

    Sstim = .01 * Istim
    n = int(pn * N)
    n_b = int((1 - pn) * N)
    if n_b < 2:
        n_b = 2

    # Create basename for the data
    basename = "Istim-{0}_g-{1}_N-{2}_pn-{3}_".format(
        Istim, g, N, pn)
    print("Running: {0}".format(basename))
    
    # path the name
    basepath = os.path.join(path, basename)

    # -- Run -------------------------------------------------------------
    Parallel(n_jobs=n_jobs)(delayed(exp)(Istim, g, N, pn)
                        for Istim, g, N, pn in params)

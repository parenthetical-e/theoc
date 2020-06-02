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
    # Create a command line interface automatically...
    fire.Fire(main)

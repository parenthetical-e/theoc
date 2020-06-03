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

    # Init
    d_H = defaultdict(list)
    d_MI = defaultdict(list)
    d_dMI = defaultdict(list)
    d_PAC = defaultdict(list)
    d_py = defaultdict(list)
    d_pxy = defaultdict(list)

    # -- Run
    iterations = range(num_trials)
    for i in iterations:
        oc_kwargs["stim_seed"] = i
        res = oscillatory_coupling(**oc_kwargs)

        # Save parts of the result...
        #
        # Entopy
        for b in res['H'].keys():
            d_H[b].append(res["H"][b])
        d_H["trial"].append(i)

        # MI
        for b in res['MI'].keys():
            d_MI[b].append(res['MI'][b])
        d_MI["trial"].append(i)

        # Change in MI, dMI
        for b in res['dMI'].keys():
            d_dMI[b].append(res['dMI'][b])
        d_dMI["trial"].append(i)

        # p(y) (oc'ed)
        for b in res['p_y'].keys():
            d_py[b].extend(res['p_y'][b])
        d_py["m"].extend(range(1, oc_kwargs["m"] + 1))
        d_py["trial"].extend([i] * oc_kwargs["m"])

        # PAC
        for b in res['PAC'].keys():
            d_PAC[b].append(res['PAC'][b])
        d_PAC["trial"].append(i)

    # -- Dump to disk!
    df_H = pd.DataFrame(d_H)
    df_H.to_csv(name + "_H.csv", index=False)
    df_MI = pd.DataFrame(d_MI)
    df_MI.to_csv(name + "_MI.csv", index=False)
    df_dMI = pd.DataFrame(d_dMI)
    df_dMI.to_csv(name + "_dMI.csv", index=False)
    df_py = pd.DataFrame(d_py)
    df_py.to_csv(name + "_py.csv", index=False)
    df_pxy = pd.DataFrame(d_pxy)
    df_pxy.to_csv(name + "_pxy.csv", index=False)
    df_PAC = pd.DataFrame(d_PAC)
    df_PAC.to_csv(name + "_PAC.csv", index=False)

    return None


if __name__ == "__main__":
    # Create a command line interface automatically...
    fire.Fire(main)

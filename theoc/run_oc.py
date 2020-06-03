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
    H = defaultdict(list)
    MI = defaultdict(list)
    dMI = defaultdict(list)
    PAC = defaultdict(list)

    # -- Run
    iterations = range(num_trials)
    for i in iterations:
        oc_kwargs["stim_seed"] = i
        res = oscillatory_coupling(**oc_kwargs)

        # Save parts of the result...
        #
        # Entopy
        for b in res['H'].keys():
            H[b].append(res["H"][b])
        H["trial"].append(i)

        # MI
        for b in res['MI'].keys():
            MI[b].append(res['MI'][b])
        MI["trial"].append(i)

        # Change in MI, dMI
        for b in res['dMI'].keys():
            dMI[b].append(res['dMI'][b])
        dMI["trial"].append(i)

        # PAC
        for b in res['PAC'].keys():
            PAC[b].append(res['PAC'][b])
        PAC["trial"].append(i)

    # -- Dump to disk!
    df_H = pd.DataFrame(H)
    df_H.to_csv(name + "_H.csv", index=False)
    df_MI = pd.DataFrame(MI)
    df_MI.to_csv(name + "_MI.csv", index=False)
    df_dMI = pd.DataFrame(dMI)
    df_dMI.to_csv(name + "_dMI.csv", index=False)
    df_PAC = pd.DataFrame(PAC)
    df_PAC.to_csv(name + "_PAC.csv", index=False)

    return None


if __name__ == "__main__":
    # Create a command line interface automatically...
    fire.Fire(main)

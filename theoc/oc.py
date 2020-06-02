#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Oscillatory coding, as LNP."""
import sys
import cloudpickle
import pandas as pd
import os
import numpy as np
# import pyentropy as en

from fakespikes import neurons, rates
from pacpy.pac import ozkurt as pacfn

from joblib import Parallel, delayed
from itertools import product
from collections import defaultdict

from theoc.lfp import create_lfps
from theoc.metrics import discrete_dist
from theoc.metrics import discrete_entropy
from theoc.metrics import discrete_mutual_information
from theoc.metrics import normalize

EPS = np.finfo(float).eps


def save_run(name, result):
    if not name.endswith(".cloudpickle"):
        name += ".cloudpickle"
    with open(name, "w") as f:
        cloudpickle.dump(result, name)


def load_run(name):
    if not name.endswith(".cloudpickle"):
        name += ".cloudpickle"
    with open(name, "r") as f:
        result = cloudpickle.load(name)
    return result


def run(num_pop=50,
        num_background=2,
        t=5,
        osc_rate=6,
        f=6,
        g=1,
        g_max=1,
        q=0.5,
        stim_rate=12,
        frac_std=.01,
        m=8,
        priv_std=0,
        dt=0.001,
        stim_seed=None,
        seed=None):
    """Run an OC experiment."""

    # -- Safety -------------------------------------------------------------
    if g > g_max:
        raise ValueError("g must be < g_max")

    # q can't be exactly 0
    q += EPS

    # -- Init ---------------------------------------------------------------
    # Poisson neurons
    backspikes = neurons.Spikes(num_background, t, dt=dt, seed=seed)
    ocspikes = neurons.Spikes(num_pop,
                              t,
                              dt=dt,
                              private_stdev=priv_std,
                              seed=seed)
    drivespikes = neurons.Spikes(num_pop,
                                 t,
                                 dt=dt,
                                 private_stdev=priv_std,
                                 seed=seed)
    times = ocspikes.times  # brevity

    # Set stim std. It must be relative to stim_rate
    stim_std = frac_std * stim_rate

    # -- Drives -------------------------------------------------------------
    # Create biases/drives
    d_bias = {}

    # Background is 2 Hz
    d_bias['back'] = rates.constant(times, 2)

    # Drives proper

    d_bias['osc'] = rates.osc(times, osc_rate, f)
    d_bias['stim'] = rates.stim(times, stim_rate, stim_std, seed=stim_seed)
    d_bias['mult'] = d_bias['stim'] * ((g_max - g + 1) * d_bias['osc'])
    d_bias['add'] = d_bias['stim'] + (g * d_bias['osc'])
    d_bias['sub'] = d_bias['stim'] - (g * d_bias['osc'])
    div = q * (g * d_bias['osc'])
    sub = (1 - q) * (g * d_bias['osc'])
    d_bias['div_sub'] = (d_bias['stim'] / div) - sub

    # -- Simulate spiking --------------------------------------------------
    # Create the background pool.
    b_spks = backspikes.poisson(d_bias['back'])

    # Create a stimulus
    stim_sp = np.hstack([drivespikes.poisson(d_bias['stim']), b_spks])

    # and then create it's OC.
    d_spikes = {}
    for k in d_bias.keys():
        d_spikes[k + "_p"] = np.hstack([ocspikes.poisson(d_bias[k]), b_spks])

    # -- LFP ----------------------------------------------------------------
    d_lfps = {}
    for k in d_spikes.keys():
        d_lfps[k] = create_lfps(d_spikes[k], tau=0.002, dt=.001)

    # -- I ------------------------------------------------------------------
    # Scale stim
    x_ref = normalize(stim_sp.sum(1))
    d_rescaled = {}
    d_rescaled["stim_p"] = x_ref

    # Calc MI and H
    d_dists = {}
    d_mis = {}
    d_hs = {}
    for k in d_spikes.keys():
        x = normalize(d_spikes[k].sum(1))
        d_rescaled[k] = x

        d_dists[k] = discrete_dist(x, m)
        d_mis[k] = discrete_mutual_information(x_ref, x, m)
        d_hs[k] = discrete_entropy(x, m)

    # -- Measure OC using PAC -----------------------------------------------
    low_f = (int(f - 2), int(f + 2))
    high_f = (80, 250)

    d_pacs = {}
    for k in d_lfps.keys():
        d_pacs[k] = pacfn(d_lfps['osc_p'], d_lfps[k], low_f, high_f)

    result = {
        'MI': d_mis,
        'H': d_hs,
        'PAC': d_pacs,
        'dist': d_dists,
        'bias': d_bias,
        'spikes': d_spikes,
        'rescaled': d_rescaled,
        'lfp': d_lfps,
        'times': times
    }

    return result
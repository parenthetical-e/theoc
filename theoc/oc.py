#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Oscillatory coding, as LNP."""
import sys
import pandas as pd
import os
import numpy as np
import pyentropy as en

from fakespikes import neurons, rates
from theoc.lfp import create_lfps

# from pacpy.pac import plv as pacfn
from pacpy.pac import ozkurt as pacfn

from joblib import Parallel, delayed
from itertools import product
from collections import defaultdict


def run(n,
        n_b,
        t,
        Iosc,
        f,
        g,
        g_max,
        q,
        Istim,
        Sstim,
        Ipri,
        dt,
        back_type,
        stim_seed=None):
    """Run an OC experiment."""

    # -----------------------------------------------------------------------
    # Safety
    if g >= g_max:
        raise ValueError("g must be < g_max")

    # -- Init ---------------------------------------------------------------
    # Poisson neurons
    backspikes = neurons.Spikes(n_b, t, dt=dt)
    ocspikes = neurons.Spikes(n, t, dt=dt, private_stdev=Ipri)
    drivespikes = neurons.Spikes(n, t, dt=dt, private_stdev=Ipri)
    times = ocspikes.times  # brevity

    # -- Drives -------------------------------------------------------------
    # Create biases/drives
    d_bias = {}

    # Background
    if back_type == 'constant':
        d_bias['back'] = rates.constant(times, 2)
    elif back_type == 'stim':
        d_bias['back'] = rates.stim(times, Istim, Sstim, seed=stim_seed)
    else:
        raise ValueError("back_type not understood")

    # Drives proper
    d_bias['osc'] = rates.osc(times, Iosc, f)
    d_bias['stim'] = rates.stim(times, Istim, Sstim, seed=stim_seed)
    d_bias['mult'] = d_bias['stim'] * ((g_max - g) * d_bias['osc'])
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
        d_lfps[k] = lfp.create_synaptic_lfps(d_spikes[k])

    # -- I ------------------------------------------------------------------
    to_calc = ('HX', 'HY', 'HXY')
    m = 8  # Per Ince's advice
    d_infos = {}
    for k in d_spikes.keys():
        d_infos[k] = en.DiscreteSystem(
            en.quantise_discrete(stim_sp.sum(1), m), (1, m),
            en.quantise_discrete(d_spikes[k].sum(1), m), (1, m))
        d_infos[k].calculate_entropies(method='pt', calc=to_calc)

    # MI
    d_mis = {}
    for k, mi in d_infos.items():
        d_mis[k] = mi.I()

    # H
    d_hs = {}
    for k, mi in d_infos.items():
        d_hs[k] = mi.H

    # -- Measure OC using PAC -----------------------------------------------
    low_f = (f - 2, f + 2)
    high_f = (80, 250)

    d_pacs = {}
    for k in d_lfps.keys():
        d_pacs[k] = pacfn(d_lfps['osc_p'], d_lfps[k], low_f, high_f)

    return {
        'MI': d_mis,
        'H': d_hs,
        'PAC': d_pacs,
        'spikes': d_spikes,
        'times': times
    }

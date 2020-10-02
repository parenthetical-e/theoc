import numpy as np
from scipy.stats.mstats import zscore


def create_lfps(spikes, tau=0.002, dt=.001):
    """Simulate LFP (1d) from spikes in channels (cols).
    Parameters
    ----------
    spikes : array-like (1d, 2d)
        A matrix of neural spikes
    tau : numeric (default: 0.001)
        The LFP estimate time constant
    dt : numeric (default: 0.001)
        ??
    Note: Assumes spikes is 1 or 2d, and *column
    oriented*
    """

    if spikes.ndim > 2:
        raise ValueError("spikes must be 1 of 2d")
    if tau < 0:
        raise ValueError("tau must be > 0")
    if dt < 0:
        raise ValueError("dt must be > 0")

    # Enforce col orientation if 1d
    if spikes.ndim == 1:
        spikes = spikes[:, np.newaxis]

    # 10 x tau (10 half lives) should be enough to span the
    # interesting parts of g, the alpha function we are
    # using to convert broadband firing to LFP
    # a technique we are borrowing from:
    #
    # http://www.ncbi.nlm.nih.gov/pubmed/20463210
    #
    # then abusing a bit (too much?).
    #
    # We want 10*tau but we have to resample to dt time first
    n_alpha_samples = int((tau * 10) / dt)
    t0 = np.linspace(0, tau * 10, n_alpha_samples)

    # Define the alpha (g notation borrow from BV's initial code)
    gmax = 0.1
    g = gmax * (t0 / tau) * np.exp(-(t0 - tau) / tau)

    # make LFP
    spsum = spikes.astype(np.float).sum(1)
    spsum /= spsum.max()

    lfps = np.convolve(spsum, g)[0:spikes.shape[0]]

    return zscore(lfps)

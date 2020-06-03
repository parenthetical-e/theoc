"""Generate model example"""
#%%
from theoc.oc import oscillatory_coupling


def example1(name="data/example1", seed=42, stim_seed=493):
    oscillatory_coupling(num_pop=50,
                         num_background=5,
                         t=5,
                         osc_rate=2,
                         f=6,
                         g=4,
                         g_max=8,
                         q=0.5,
                         stim_rate=20,
                         frac_std=0.01,
                         m=20,
                         dt=0.001,
                         stim_seed=stim_seed,
                         seed=seed,
                         save=name)


if __name__ == "__main__":
    print(">>> Running example 1")
    example1()
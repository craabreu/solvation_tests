import itertools
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import figstyle

cases = ['piny']
timesteps = [6, 9, 15, 30, 45, 90]

# Intermolecular radial distribution functions:
rdf = {case:[] for case in cases}
for dt, case in itertools.product(timesteps, cases):
    rdf[case].append(pd.read_csv(f'{case}/results/sinr-{dt:02d}fs_rdf.csv', skipinitialspace=True))

for case in cases:
    fig, ax = plt.subplots(3, 1, figsize=(3.37,5.6), sharex=True)
    fig.suptitle(f'Radial distribution functions ({case})')
    fig.subplots_adjust(hspace=0.1)
    ax[-1].set_xlabel('Distance (\\AA)')
    for dt, gr in zip(timesteps, rdf[case]):
        distance = gr['Distance [pm]']/100
        for i, pair in enumerate(['O-O', 'O-H', 'H-H']):
            ax[i].plot(distance, gr[f'g({pair})'], label=f'{dt} fs')
            ax[i].set_ylabel(f'g({pair})')
    ax[2].legend(loc='lower right', ncol=2)
    fig.savefig(f'{case}_rdf.png')

# Bond length distributions:
bond = {case:[] for case in cases}
for dt, case in itertools.product(timesteps, cases):
    bond[case].append(pd.read_csv(f'{case}/results/sinr-{dt:02d}fs_bond.csv', skipinitialspace=True))

for case in cases:
    fig, ax = plt.subplots(1, 1, figsize=(3.37,2.3), sharex=True)
    fig.suptitle(f'Bond length distributions ({case})')
    ax.set_xlabel('Distance (\\AA)')
    for dt, gr in zip(timesteps, bond[case]):
        distance = gr['# Distance [pm]']/100
        ax.plot(distance, gr['g(r)'], label=f'{dt} fs')
        ax.set_ylabel(f'frequency')
    ax.legend(loc='upper left', ncol=1)
    fig.savefig(f'{case}_bond.png')

# Angle distributions:
angle = {case:[] for case in cases}
for dt, case in itertools.product(timesteps, cases):
    angle[case].append(pd.read_csv(f'{case}/results/sinr-{dt:02d}fs_angle.csv', skipinitialspace=True))

for case in cases:
    fig, ax = plt.subplots(1, 1, figsize=(3.37,2.3), sharex=True)
    fig.suptitle(f'Angle distributions ({case})')
    ax.set_xlabel('Angle (\\textdegree)')
    for dt, gr in zip(timesteps, angle[case]):
        distance = gr['# Angle (degree)']
        ax.plot(distance, gr['Occurrence'], label=f'{dt} fs')
        ax.set_ylabel(f'frequency')
    ax.legend(loc='upper left', ncol=1)
    fig.savefig(f'{case}_angle.png')

plt.show()

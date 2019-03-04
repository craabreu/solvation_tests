import itertools
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import figstyle
import os

tools = ['piny', 'openmm']
timesteps = ['0p5', '01', '03', '06', '09', '15', '30', '45', '90']

def data(type):
    repo = {tool:[] for tool in tools}
    for dt, tool in itertools.product(timesteps, tools):
        file = f'{tool}/results/sinr-{dt}fs_{type}.csv'
        if os.path.isfile(file):
            repo[tool].append(pd.read_csv(file, skipinitialspace=True))
    return repo

# Intermolecular radial distribution functions:
rdf = data('rdf')
for tool in tools:
    fig, ax = plt.subplots(3, 1, figsize=(3.37,5.6), sharex=True)
    fig.suptitle(f'Radial distribution functions ({tool})')
    fig.subplots_adjust(hspace=0.1)
    ax[-1].set_xlabel('Distance (\\AA)')
    for dt, gr in zip(timesteps, rdf[tool]):
        distance = gr['Distance [pm]']/100
        for i, pair in enumerate(['O-O', 'O-H', 'H-H']):
            ax[i].plot(distance, gr[f'g({pair})'], label=f'{dt} fs')
            ax[i].set_ylabel(f'g({pair})')
    ax[2].legend(loc='lower right', ncol=2)
    fig.savefig(f'{tool}_rdf.png')

# Bond length distributions:
bond = data('bond')
for tool in tools:
    fig, ax = plt.subplots(1, 1, figsize=(3.37,2.3), sharex=True)
    fig.suptitle(f'Bond length distributions ({tool})')
    ax.set_xlabel('Distance (\\AA)')
    for dt, gr in zip(timesteps, bond[tool]):
        distance = gr['# Distance [pm]']/100
        ax.plot(distance, gr['g(r)'], label=f'{dt} fs')
        ax.set_ylabel(f'frequency')
    ax.legend(loc='upper left', ncol=1)
    fig.savefig(f'{tool}_bond.png')

# Angle distributions:
angle = data('angle')
for tool in tools:
    fig, ax = plt.subplots(1, 1, figsize=(3.37,2.3), sharex=True)
    fig.suptitle(f'Angle distributions ({tool})')
    ax.set_xlabel('Angle (\\textdegree)')
    for dt, gr in zip(timesteps, angle[tool]):
        distance = gr['# Angle (degree)']
        ax.plot(distance, gr['Occurrence'], label=f'{dt} fs')
        ax.set_ylabel(f'frequency')
    ax.legend(loc='upper left', ncol=1)
    fig.savefig(f'{tool}_angle.png')

plt.show()

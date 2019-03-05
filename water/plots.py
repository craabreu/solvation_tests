import itertools
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import figstyle
import os

tools = ['piny', 'openmm']

def data(type, timesteps):
    repo = {tool:[] for tool in tools}
    for dt, tool in itertools.product(timesteps, tools):
        file = '{}/results/sinr-{}fs_{}.csv'.format(tool, dt.replace('.', 'p'), type)
        if os.path.isfile(file):
            repo[tool].append(pd.read_csv(file, skipinitialspace=True))
    return repo

# Intermolecular radial distribution functions:
def plot_rdfs(timesteps):
    rdf = data('rdf', timesteps)
    for tool in tools:
        fig, ax = plt.subplots(3, 1, figsize=(3.37,5.6), sharex=True)
        fig.suptitle(f'Radial distribution functions ({tool})')
        fig.subplots_adjust(hspace=0.1)
        ax[-1].set_xlabel('Distance (\\AA)')
        for dt, gr in zip(timesteps, rdf[tool]):
            distance = gr['Distance [pm]']/100
            for i, pair in enumerate(['O-O', 'O-H', 'H-H']):
                ax[i].plot(distance, gr[f'g({pair})'], label='{} fs'.format(dt))
                ax[i].set_ylabel(f'g({pair})')
        ax[2].legend(loc='lower right', ncol=2)
        fig.savefig(f'{tool}_rdf.png')

# Bond length distributions:
def plot_bonds(timesteps):
    bond = data('bond', timesteps)
    for tool in tools:
        fig, ax = plt.subplots(1, 1, figsize=(3.37,2.3), sharex=True)
        fig.suptitle(f'Bond length distributions ({tool})')
        ax.set_xlabel('Distance (\\AA)')
        for dt, gr in zip(timesteps, bond[tool]):
            distance = gr['# Distance [pm]']/100
            ax.plot(distance, gr['g(r)'], label='{} fs'.format(dt))
            ax.set_ylabel(f'frequency')
        ax.legend(loc='upper left', ncol=1)
        fig.savefig(f'{tool}_bond.png')

# Angle distributions:
def plot_angles(timesteps):
    angle = data('angle', timesteps)
    for tool in tools:
        fig, ax = plt.subplots(1, 1, figsize=(3.37,2.3), sharex=True)
        fig.suptitle(f'Angle distributions ({tool})')
        ax.set_xlabel('Angle (\\textdegree)')
        for dt, gr in zip(timesteps, angle[tool]):
            distance = gr['# Angle (degree)']
            ax.plot(distance, gr['Occurrence'], label='{} fs'.format(dt))
            ax.set_ylabel(f'frequency')
        ax.legend(loc='upper left', ncol=1)
        fig.savefig(f'{tool}_angle.png')

# Combined bond-angle distributons:
def plot_combined(timestep_pairs):
    npairs = len(timestep_pairs)
    for tool in tools:
        fig, ax = plt.subplots(npairs, 1, figsize=(3.37,npairs*2.3), sharex=True)
        if npairs == 1:
            ax = [ax]
        fig.suptitle(f'Combined bond-angle distributions ({tool})')
        ax[-1].set_xlabel('Distance (\\AA)')
        for i, timesteps in enumerate(timestep_pairs):
            combined = data('combined', timesteps)
            for dt, gr, style in zip(timesteps, combined[tool], ['solid', 'dashed']):
                X = gr.values[:, 0]/100  # Distances
                Y = np.array([float(y) for y in gr.columns[1:]])  # Angles
                Z = gr.values[:, 1:]
                cs = ax[i].contour(*np.meshgrid(X, Y), Z, linestyles=style)
                cs.collections[0].set_label('{} fs'.format(dt))
            ax[i].set_ylabel('Angle (\\textdegree)')
            ax[i].legend(loc='lower left', ncol=1)
        fig.savefig(f'{tool}_combined.png')

plot_rdfs(['0.5', '01', '03', '06', '09', '15', '30', '45', '90'])
plot_bonds(['0.5', '01', '03', '06', '09', '15', '30', '45', '90'])
plot_angles(['0.5', '01', '03', '06', '09', '15', '30', '45', '90'])
plot_combined([('0.5', '90'), ('06', '90')])
# plt.show()

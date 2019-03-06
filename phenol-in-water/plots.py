import itertools
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import figstyle
import os

dt_scaling = 'log'
tools = ['piny', 'openmm']
step_size = {'0.5': 0.5}
label = {'0.5': '0.5 fs (*)'}
for case in ['01', '03', '06', '09', '15', '30', '45', '90']:
    step_size[case] = float(case)
    label[case] = '{} fs'.format(int(case))

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
    fig, ax = plt.subplots(1, 1, figsize=(3.37,2.3))
    fig.suptitle(f'Radial distribution functions (openmm)')
    ax.set_xlabel('Distance (\\AA)')
    for dt, gr in zip(timesteps, rdf['openmm']):
        distance = gr['Distance [pm]']/100
        ax.plot(distance, gr['g(r)'], label=label[dt])
    ax.legend(loc='lower right', ncol=2)
    fig.savefig(f'openmm_rdf.png')

# Bond length distributions:
def plot_bonds(timesteps):
    bond = data('bond', timesteps)
    for tool in tools:
        fig, ax = plt.subplots(1, 1, figsize=(3.37,2.3), sharex=True)
        fig.suptitle(f'Bond length distributions ({tool})')
        ax.set_xlabel('Distance (\\AA)')
        for dt, gr in zip(timesteps, bond[tool]):
            distance = gr['# Distance [pm]']/100
            ax.plot(distance, gr['g(r)'], label=label[dt])
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
            ax.plot(distance, gr['Occurrence'], label=label[dt])
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
                cs.collections[0].set_label(label[dt])
            ax[i].set_ylabel('Angle (\\textdegree)')
            ax[i].legend(loc='lower left', ncol=1)
        fig.savefig(f'{tool}_combined.png')

# Combined bond-bond distributons:
def plot_bond_bond(timestep_pairs):
    npairs = len(timestep_pairs)
    for tool in tools:
        fig, ax = plt.subplots(npairs, 1, figsize=(3.37,npairs*2.3), sharex=True)
        if npairs == 1:
            ax = [ax]
        fig.suptitle(f'Combined bond-bond distributions ({tool})')
        ax[-1].set_xlabel('Distance (\\AA)')
        for i, timesteps in enumerate(timestep_pairs):
            combined = data('bbdf', timesteps)
            for dt, gr, style in zip(timesteps, combined[tool], ['solid', 'dashed']):
                X = gr.values[:, 0]/100
                Y = np.array([float(y)/100 for y in gr.columns[1:]])
                Z = gr.values[:, 1:]
                cs = ax[i].contour(*np.meshgrid(X, Y), Z, linestyles=style)
                cs.collections[0].set_label(label[dt])
            ax[i].set_ylabel('Distance (\\AA)')
            ax[i].legend(loc='lower left', ncol=1)
            ax[i].set_aspect(1.0)
        fig.savefig(f'{tool}_bond_bond.png')

# Average bonds and angles:
def plot_bond_and_angle_averages():
    fig, ax = plt.subplots(2, 1, figsize=(3.37,4.6), sharex=True)
    fig.suptitle(f'Average bond lengths and angles')
    ax[-1].set_xlabel('Time step size (fs)')
    for i, type in enumerate(['bond', 'angle']):
        for tool in tools:
            df = pd.read_csv(f'{tool}/results/{type}_stats.csv')
            dt, mean = df['dt'], df['mean']
            if type == 'bond':
                mean /= 100
            ax[i].plot(dt, mean, marker='o', label=tool)
            ax[i].legend(loc='lower left', ncol=1)
    ax[0].set_xscale(dt_scaling)
    ax[0].set_ylabel('Bond length (\\AA)')
    ax[0].legend(loc='upper right', ncol=1, title='$r_0 = 1.012$ \\AA')
    ax[1].set_xscale(dt_scaling)
    ax[1].set_ylabel('Angle (\\textdegree)')
    ax[1].legend(loc='lower right', ncol=1, title='$\\theta_0 = 113.24$\\textdegree')
    fig.savefig('average_bonds_and_angles.png')

# Properties:
def plot_properties():
    openmm = pd.read_csv('openmm/results/properties.csv')
    piny = pd.read_csv('piny/results/properties.csv')

    fig, ax = plt.subplots(2, 1, figsize=(3.37,4.6), sharex=True)
    fig.suptitle(f'Average Properties')
    ax[-1].set_xlabel('Time step size (fs)')

    Econv = 627.50921*4.184

    energy = ax[0]
    energy.set_xscale(dt_scaling)
    energy.set_ylabel('Potential Energy (kJ/mol)')
    # E_lrc = -63.2297879351536
    energy.plot(openmm['dt'], openmm['PotEng'], marker='o', label='openmm')
    energy.plot(piny['dt'], Econv*piny['Etotal'], marker='o', label='piny')
    energy.legend(loc='upper left', ncol=1)

    pressure = ax[1]
    pressure.set_xscale(dt_scaling)
    pressure.set_ylabel('Pressure (atm)')
    pressure.plot(openmm['dt'], openmm['Press'], marker='o', label='openmm')

    N = 512*3
    V = 24.653**3  # A³
    kB = 8.31451E-7  # Boltzmann constant in Da*A²/(fs²*K)
    Pconv = 1.6388244954E+8  # Da/(A*fs²) to atm
    T = 298.15  # K
    P = piny['Ptotal'] - Pconv*N*kB*(piny['Temp'] - T)/V
    pressure.plot(piny['dt'], P, marker='o', label='piny')
    pressure.legend(loc='upper left', ncol=1)

    fig.savefig('average_properties.png')

all = ['0.5', '01', '03', '06', '09', '15', '30', '45', '90']
plot_rdfs(all)
# plot_bonds(all)
# plot_angles(all)
# plot_combined([('0.5', '90'), ('06', '90')])
# plot_bond_bond([('0.5', '90'), ('06', '90')])
# plot_bond_and_angle_averages()
# plot_properties()
plt.show()

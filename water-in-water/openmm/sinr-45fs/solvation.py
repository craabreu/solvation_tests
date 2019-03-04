import argparse
import atomsmm
import pandas as pd

import math
import time

from sys import stdout
from simtk import openmm
from simtk import unit
from simtk.openmm import app

parser = argparse.ArgumentParser()
parser.add_argument('--steps', dest='steps', help='steps per state', type=int, required=True)
parser.add_argument('--device', dest='device', help='the GPU device', default='None')
parser.add_argument('--seed', dest='seed', help='the RNG seed', type=int, default=0)
parser.add_argument('--platform', dest='platform', help='the computation platform', default='CUDA')
args = parser.parse_args()

seed = int(1000*time.time()) % 16384 if args.seed == 0 else args.seed
print(f'Employed RNG seed is {seed}')

solute = 'water'
solvent = 'water'
base = '{}-in-{}'.format(solute, solvent)
platform_name = args.platform
methods = {1:'Langevin', 2:'SIN-R', 3:'NHL-R'}
method = methods[2]

steps_per_state = args.steps
rigid_water = False
use_barostat = False
split_exceptions = False

dt = 45*unit.femtoseconds
temp = 298.15*unit.kelvin
rcut = 12*unit.angstroms
rswitch = 11*unit.angstroms
rcutIn = 8*unit.angstroms
rswitchIn = 5*unit.angstroms
tau = 10*unit.femtoseconds
gamma = 0.1/unit.femtoseconds
reportInterval = 2
barostatInterval = 25 if use_barostat else 0

platform = openmm.Platform.getPlatformByName(platform_name)
properties = dict(Precision='mixed') if platform_name == 'CUDA' else dict()
if args.device != 'None':
    properties['DeviceIndex'] = args.device

pdb = app.PDBFile(f'water.pdb')
residues = [atom.residue.name for atom in pdb.topology.atoms()]
#solute_atoms = set(i for (i, name) in enumerate(residues) if name == 'aaa')
solute_atoms = set(range(3))

forcefield = app.ForceField(f'water.xml')
openmm_system = forcefield.createSystem(pdb.topology,
                                        nonbondedMethod=openmm.app.PME,
                                        nonbondedCutoff=rcut,
                                        rigidWater=rigid_water,
                                        removeCMMotion=False)

nbforce = openmm_system.getForce(atomsmm.findNonbondedForce(openmm_system))
nbforce.setUseSwitchingFunction(True)
nbforce.setSwitchingDistance(rswitch)
nbforce.setUseDispersionCorrection(True)

solvation_system = atomsmm.SolvationSystem(openmm_system, solute_atoms,
                                           use_softcore=False,
                                           split_exceptions=split_exceptions)
solvation_system = atomsmm.RESPASystem(solvation_system, rcutIn, rswitchIn, fastExceptions=False)

if barostatInterval > 0:
    barostat = openmm.MonteCarloBarostat(1*unit.atmospheres, temp, barostatInterval)
    barostat.setRandomNumberSeed(seed)
    solvation_system.addForce(barostat)

if method == 'Langevin':
    integrator = openmm.LangevinIntegrator(temp, 1.0/unit.picoseconds, dt)
elif not rigid_water:
    Method = atomsmm.NHL_R_Integrator if method == 'NHL-R' else atomsmm.NewMethodIntegrator
    integrator = Method(dt, [6, 15, 1], temp, tau, gamma)
else:
    raise Exception("Wrong method and/or rigidity option")
integrator.setRandomNumberSeed(seed)

simulation = openmm.app.Simulation(pdb.topology, solvation_system, integrator, platform, properties)
simulation.context.setPositions(pdb.positions)
simulation.context.setVelocitiesToTemperature(temp, seed)

states_data = pd.read_csv('alchemical_states.inp', sep='\s+', comment='#')
parameterStates = states_data[['lambda_vdw', 'lambda_coul']]
for state in reversed(states_data.index):
    if state <=	3:
        for name, value in parameterStates.iloc[state].items():
            simulation.context.setParameter(name, value)
            print(f'{name} = {value}')
        dataReporter = atomsmm.ExtendedStateDataReporter(stdout, reportInterval, separator=',',
            step=True, potentialEnergy=True, temperature=True, density=barostatInterval > 0,
            speed=True, extraFile=f'{base}_data-{state:02d}.csv')
        multistateReporter = atomsmm.ExtendedStateDataReporter(f'{base}_energy-{state:02d}.csv',
            reportInterval, separator=',', step=True, globalParameterStates=parameterStates)
        simulation.reporters = [dataReporter, multistateReporter]
        simulation.step(steps_per_state)


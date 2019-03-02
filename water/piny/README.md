PINY Tests
==========

The objective of this section is to test how the average properties of [SPC/Fw] water computed using
the SIN(R) method, as implemented in [PINY], vary with the size of the outer time step.

Some modifications were made to the original example available in [PINY]:

1. File `coords.init`: box vectors were changed to produce a cubic box with side length of 24.653
angstroms, thus resulting in a density of 1.022 g/cc.

2. File `pi_md.inter`: Cut-off distance was changed to 12.0 angstroms.

3. File `pi_md.bond`: Equilibrium distance changed to 1.012 angstroms.

4. File `pi_md.bend`: Equilibrium angle changed to 113.24 degrees.

5. File `water.parm`: Oxygen and hydrogen charges changes to -0.82 and 0.41, respectively.

6. File `water.input`:

    - Temperature changed to 298.15 K

    - Nose-Hoover chain length changed to 1

    - Yoshida-Suzuki scheme disabled

    - Nose-Hoover splitting changed to 5

    - Explicit definition of potential healing length of 1 angstrom


Execution
=========

The simulations can be executed in a [Slurm]-based cluster with available [GNU Parallel] installation by using:

    sbatch slurm_job.sh


Trajectory Analysis
===================

Trajectories are converted to the `xyz` format:

    ./convert_trajectories 1 3 6 9 15 30 45 90


[SPC/Fw]: https://doi.org/10.1063/1.2136877
[PINY]: https://github.com/craabreu/PINY
[Slurm]: https://slurm.schedmd.com
[GNU Parallel]: https://www.gnu.org/software/parallel/

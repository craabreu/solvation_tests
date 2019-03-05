#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=14
#SBATCH --time=1:00:00
#SBATCH --mem=20GB
#SBATCH --job-name=analyze_sinr
#SBATCH --mail-type=ALL
#SBATCH --mail-user=ca2356@nyu.edu
#SBATCH --output=slurm_%j.out

#module purge
#module load gnu8/8.2.0
#module load openmpi3/3.1.2
#module load fftw/3.3.8

#parallel ./analyze_sinr.sh piny ::: 06 09 15 30 45 90
parallel ./analyze_sinr.sh openmm ::: 03 06 09 15 30 45 90

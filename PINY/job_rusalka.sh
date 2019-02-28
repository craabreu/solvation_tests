#!/usr/bin/env bash
#SBATCH -J sinr           # Job name
#SBATCH -o job.%j.out     # Name of stdout output file
#SBATCH -N 1              # Total number of nodes requested
#SBATCH -n 7              # Total number of mpi tasks requested
#SBATCH --mem=10GB        # To specify required memory per node
#SBATCH -t 90:00:00       # Run time (hh:mm:ss) - 24 hours
#SBATCH --mail-type=ALL
#SBATCH --mail-user=ca2356@nyu.edu

module purge
module load gnu8/8.2.0
module load openmpi3/3.1.2
module load fftw/3.3.8

parallel ./run_sinr.sh ::: 03 06 09 15 30 45 90

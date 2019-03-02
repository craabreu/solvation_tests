#!/usr/bin/env bash
name=sinr-${1}fs
cd $name

# Clean directory and run simulation:
./tidy
./run > $name.output

# Convert trajectory file to xyz format:
python ../conf-to-traj.py --out $name.xyz --decimal 8 water.confp

#!/usr/bin/env bash
# Usage: ./analyze_sinr.sh [piny/openmm] [delta-t]
./compute_rdf.sh $@
./compute_bond.sh $@
./compute_angle.sh $@
./compute_sdf.sh $@

#!/usr/bin/env bash
for dt in $@; do
    name=$(printf "sinr-%02dfs" $dt)
    cd $name
    python ../conf-to-traj.py --out $name.xyz --decimal 8 water.confp
    cd ..
done

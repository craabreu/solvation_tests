#!/usr/bin/env bash
for dt in $@; do
    name=$(printf "sinr-%02dfs" $dt)
    python conf-to-traj.py --out $name.xyz --decimal 8 $name/water.confp
done

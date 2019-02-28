#!/bin/bash

case+=("1")
nsteps+=("3600000")
device+=("0")

case+=("3")
nsteps+=("1200000")
device+=("1")

case+=("6")
nsteps+=("600000")
device+=("2")

case+=("9")
nsteps+=("400000")
device+=("3")

case+=("15")
nsteps+=("240000")
device+=("0")

case+=("30")
nsteps+=("120000")
device+=("1")

case+=("45")
nsteps+=("80000")
device+=("2")

case+=("90")
nsteps+=("40000")
device+=("3")

python simulate.py --device ${device[$1]} --timestep ${case[$1]} --nsteps ${nsteps[$1]}

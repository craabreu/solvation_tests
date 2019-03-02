#!/bin/bash

case+=("01")
nsteps+=("3600000")
device+=("0")

case+=("03")
nsteps+=("1200000")
device+=("1")

case+=("06")
nsteps+=("600000")
device+=("2")

case+=("09")
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

cd sinr-${case[$1]}fs
python simulate.py --device ${device[$1]} --timestep ${case[$1]} --nsteps ${nsteps[$1]}

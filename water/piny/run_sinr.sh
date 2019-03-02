#!/usr/bin/env bash
cd sinr-${1}fs

# Clean directory and run simulation:
./tidy
./run > sinr-${1}fs.output

# Convert trajectory file to xyz format:
python ../conf-to-traj.py --out $1.xyz --decimal 8 water.confp

# Compute radial distribution functions:
mkdir -p rdf
cd rdf
../../../../travis/exe/travis -i ../../../travis_rdf.inp -p ../$1.xyz
gOO="rdf_H2O_#2_H2O_[Or_Oo].csv"
gOH="rdf_H2O_#2_H2O_[Or_Ho].csv"
gHH="rdf_H2O_#2_H2O_[Hr_Ho].csv"
gIntra="rdf_H2O_#2_H2O_[Or_Ho].csv"
paste -d"," <(cut -d";" -f1 $gOO | sed 's/# //g')  \
            <(cut -d";" -f2 $gOO | sed 's/g(r)/g(O-O)/g') \
            <(cut -d";" -f2 $gOH | sed 's/g(r)/g(O-H)/g') \
            <(cut -d";" -f2 $gHH | sed 's/g(r)/g(H-H)/g') > ../${1}_rdf.csv
sed 's/;/,/g' $gIntra > ../${1}_bond.csv

#!/usr/bin/env bash
name=sinr-${1}fs
cd $name

# Clean directory and run simulation:
./tidy
./run > $name.output

# Convert trajectory file to xyz format:
python ../conf-to-traj.py --out $name.xyz --decimal 8 water.confp

# Compute radial distribution functions:
mkdir -p rdf
cd rdf
../../../../travis/exe/travis -i ../../../travis_rdf.inp -p ../$name.xyz
gOO="rdf_H2O_#2_H2O_[Or_Oo].csv"
gOH="rdf_H2O_#2_H2O_[Or_Ho].csv"
gHH="rdf_H2O_#2_H2O_[Hr_Ho].csv"
gIntra="rdf_H2O_#2_H2O_[Or_Ho].csv"
paste -d"," <(cut -d";" -f1 $gOO | sed 's/# //g')  \
            <(cut -d";" -f2 $gOO | sed 's/g(r)/g(O-O)/g') \
            <(cut -d";" -f2 $gOH | sed 's/g(r)/g(O-H)/g') \
            <(cut -d";" -f2 $gHH | sed 's/g(r)/g(H-H)/g') > ../${name}_rdf.csv
sed 's/;/,/g' $gIntra > ../${name}_bond.csv

#!/usr/bin/env bash
dir=$1
name=sinr-${2}fs

# Compute radial distribution functions:
cd $dir/$name
mkdir -p bdf
cd bdf
root=../../../..
$root/travis/exe/travis -i $root/water/travis_bond.inp -p ../$name.xyz > ${name}_bond.output
file="rdf_H2O_#2_[Or_Hr].csv"
sed 's/;/,/g' $file > $root/water/$dir/results/${name}_bond.csv

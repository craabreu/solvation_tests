#!/usr/bin/env bash
dir=$1
name=sinr-${2}fs

# Compute radial distribution functions:
cd $dir/$name
mkdir -p rdf
cd rdf
root=../../../..
$root/travis/exe/travis -i $root/water/travis_bond.inp -p ../$name.xyz > ../${name}_bond.output
gIntra="rdf_H2O_#2_H2O_[Or_Ho].csv"
sed 's/;/,/g' $gIntra > ../${name}_bond.csv

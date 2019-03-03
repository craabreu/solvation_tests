#!/usr/bin/env bash
dir=$1
name=sinr-${2}fs

# Compute radial distribution functions:
cd $dir/$name
mkdir -p rdf
cd rdf
root=../../../..
$root/travis/exe/travis -i $root/water/travis_bond.inp -p ../$name.xyz > ../${name}_bond.output
gIntra="rdf_H2O_#2_[Or_Hr].csv"
sed 's/;/,/g' $gIntra > $root/water/$dir/results/${name}_bond.csv

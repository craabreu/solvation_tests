#!/usr/bin/env bash
dir=$1
name=sinr-${2}fs

# Compute radial distribution functions:
cd $dir/$name
mkdir -p rdf
cd rdf
root=../../../..
$root/travis/exe/travis -i $root/phenol-in-water/travis_rdf.inp -p ../$name.xyz #> ${name}_rdf.output
file="rdf_C6H6O_#2_H2O_[#2r_#2o].csv"
cp $file $root/phenol-in-water/$dir/results/${name}_rdf.csv

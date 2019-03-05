#!/usr/bin/env bash
dir=$1
name=sinr-${2}fs

# Compute radial distribution functions:
cd $dir/$name
mkdir -p bbdf
cd bbdf
root=../../../..
$root/travis/exe/travis -i $root/water/travis_bbdf.inp -p ../$name.xyz > ${name}_bbdf.output
file="cdf_2_rdf[O1r_H1r]_rdf[O1r_H2r]_matrix.csv"
sed 's/;/,/g' $file > $root/water/$dir/results/${name}_bbdf.csv

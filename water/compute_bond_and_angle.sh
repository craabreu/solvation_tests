#!/usr/bin/env bash
dir=$1
name=sinr-${2}fs

# Compute radial distribution functions:
cd $dir/$name
mkdir -p cdf
cd cdf
root=../../../..
$root/travis/exe/travis -i $root/water/travis_cdf.inp -p ../$name.xyz > ${name}_cdf.output

file="rdf_H2O_#2_[Or_Hr].csv"
sed 's/;/,/g' $file > $root/water/$dir/results/${name}_bond.csv

file="adf_H2O_#2_[O1r_H1r]-[O1r_H2r].csv"
sed 's/;/,/g' $file > $root/water/$dir/results/${name}_angle.csv

file="cdf_2_rdf[Or_Hr]_adf[O1r_H1r]-[O1r_H2r]_matrix.csv"
sed 's/;/,/g' $file > $root/water/$dir/results/${name}_combined.csv

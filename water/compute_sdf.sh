#!/usr/bin/env bash
dir=$1
name=sinr-${2}fs

# Compute radial distribution functions:
cd $dir/$name
mkdir -p sdf
cd sdf
root=../../../..
$root/travis/exe/travis -i $root/water/travis_sdf.inp -p ../$name.xyz #> ${name}_sdf.output
Odist="sdf_H2O_#2O1H1_H2O_O.s2.cube"
Hdist="sdf_H2O_#2O1H1_H2O_H.s2.cube"
molecule="ref_h2o_#2_o1_h1.xyz"
prefix=$root/water/$dir/results/${name}_sdf
cp $Odist ${prefix}_O.cube
cp $Hdist ${prefix}_H.cube
cp $molecule ${prefix}_mol.xyz

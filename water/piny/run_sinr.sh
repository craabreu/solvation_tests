#!/usr/bin/env bash
name=sinr-${1}fs
cd $name

# Clean directory and run simulation:
#./tidy
#./run > $name.output

# Convert trajectory file to xyz format:
#python ../conf-to-traj.py --out $name.xyz --decimal 8 water.confp

# Extract properties:
#../extract_properties.sh $1 > ${name}_properties.csv
properties='Temp Einter Eintra Etotal Pinter Pintra Ptotal'
# title='dt'
# for prop in $properties; do
#     title+=,$prop,rmse[$prop]
# done

dt=$(echo $1 | sed 's/p/./')
values=$(postlammps -d comma -p -c 83 -nt ineff $properties < ${name}_properties.csv | \
         cut -d',' -f2,3 | \
         tr '\n' ',' | \
         sed 's/,$//')
line=$(echo "$dt,$values")
eval "sed -i 's/^$dt.*/$line/' ../results/properties.csv"

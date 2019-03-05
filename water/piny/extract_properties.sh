#!/usr/bin/env bash
name=sinr-${1}fs
file=${name}.output

paste -d, \
    <(echo "Temp"; grep "^Atm Temperature" $file | cut -c 21- | cut -d" " -f1) \
    <(echo "Einter"; grep "^Intermol PE" $file | cut -c 19- | cut -d" " -f1) \
    <(echo "Eintra"; grep "^Intramol PE" $file | cut -c 21- | cut -d" " -f1) \
    <(echo "Etotal"; grep "^Total PE" $file | cut -c 19- | cut -d" " -f1) \
    <(echo "Pinter"; grep "^Inter Pressure" $file | cut -c 20- | cut -d" " -f1) \
    <(echo "Pintra"; grep "^Intra Pressure" $file | cut -c 20- | cut -d" " -f1) \
    <(echo "Ptotal"; grep "^Total Pressure" $file | cut -c 20- | cut -d" " -f1)

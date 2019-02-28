#!/usr/bin/env bash
cd sinr-${1}fs
./tidy
./run > ../sinr-${1}fs.output

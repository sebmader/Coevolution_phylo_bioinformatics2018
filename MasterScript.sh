#! /bin/bash

#This program combines phylogenetic trees of two coevolving species with their coevolving trait values.
#It outputs two trees face-to-face and prints the mean trait value per species in the trees.

#This script calls all the scripts for the single steps of the operation

python genload.py

Rscript workingRscript.R


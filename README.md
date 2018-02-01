# Coevolution_phylo_bioinformatics2018
The program provided in this repository visualizes coevolution of traits of two coevolving species. It produces two aligned phylogenetic trees facing each other and providing the mean trait value per species.
## Composition
This program is separated in two segments: The first part is a python script that askes for a csv file as input which contains species names, a group ID (which tree it should be part of), the trait examined and the individual trait values. It uses the species names to download genomic data from GenBank. So far, group one is using ribosomal DNA whereas group two uses mitochondrial DNA. This is due to our example data set that contains plants (group one) and their insect pollinators (group two). After downloading the sequences in fasta-format, they are being combined per group and converted into a format to be alligned. Thereafter, the sequences are used to create a newick tree file.
The second segment of the program is a R script that usees the newick tree file to plot the trees as final output.
## Installation
This program uses all following packages that need to be installed beforehand: 
* sadfasdf
## Usage

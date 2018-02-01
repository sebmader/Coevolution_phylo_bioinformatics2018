#load required packages
library(phangorn)
library(ape)
library(seqinr)

# Load in the phyml tree output
tree=read.tree("Output_phyllip1.phy_phyml_tree")
tree.phylo=as.phylo(tree) # Save the tree as a .phylo format
tree2=read.tree("Output_phyllip2.phy_phyml_tree")
tree2.phylo=as.phylo(tree2)
tree
tree$tip.label # These are the current names saved in the trees
string1=readLines("fullnames1") # Saves the new names with charactervalues
string1
test = tree$tip.label # Saves the tree names
sortvect=order(test) # Saves the order in which the tree names are (based on alphabetical order)
sortvect
test2=sort(string1) # Saves the order of the new names
test3=test2[order(sortvect)] # Saves the new names in the order of the old names
tree$tip.label=test3 # Swaps the old names for the new ones

string2=readLines("fullnames2") # does the same things for the second group

test = tree2$tip.label
test
sortvect=order(test)
sortvect
test2=test[sortvect]
test2
test2=sort(string2)
test3=test2[order(sortvect)]
tree2$tip.label=test3

png(filename="cophylotree.png", width = 720, height =480) # Makes it possible to save the file in a .png
cophyloplot(tree, tree2, assoc = NULL, length.line = 4, space = 28, gap = 3) # Creates a cophylo tree which displays both trees next to each other
dev.off() # turns off the png program

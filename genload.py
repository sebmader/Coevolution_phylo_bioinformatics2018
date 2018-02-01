#! /usr/bin/env python

from Bio import Entrez # Import the Entrez module from biopython which allows us to search and download information from GenBank
from Bio.Seq import Seq
from Bio import SeqIO
import os # os allows for usage of the bash shell
import re # re allows for the use of regular expressions in python

input=raw_input("Enter input file: ") # This allows the user to type the name of the input file in the terminal

groups=(1,2) # Since we are creating two phylogenies based on two groups in the input file, everything must be done twice

for i in groups: # This will run through each command twice, once for each group, in order to produce the two phylogeny trees that we want
	print "Initiating group "+str(i)+" conversion..." # Prints a status report to know that the script is actually running
	os.system('tail -n +2 ' + input + ' | cut -f 1,2,3 -d "," | sort -n -k 1 -t "," | grep '+str(i)+' | cut -f 2,3 -d "," | tr "," "+" | uniq > tempformat'+str(i)+'.txt') # The os.system() command allows for bash commands to be used. This bash command is used to only select the genus and species names and add a + inbetween the two. This is required for the Entrez searchquery later, where a + signifies a space. This is then stored in tempformat (with the group number) in order to use the results in the rest of the python script.
	vari=open("tempformat"+str(i)+".txt", 'r') # Opens the created tempformat file which now has all genus and species names of a certain group. The 'r' is used to read this file instead of writing to it.
	vari=vari.read() # This stores the text from tempformat in a statement
	list=vari.split("\n") # This creates a list of all genus+species names. Since the last line also contains a line ending, an empty string is added at the end of the list.
	del list[len(list)-1] # This removes the empty string at the end of the list
	OutFileName = input+str(i)+'.fasta' # Creates a name for an output file based on the input name
	OutFile = open(OutFileName, 'a') # Opens the a file with the outfile name. The 'a' stands for append and allows entries to be added to the file instead of overwriting the file.
	Entrez.email = "basti.mader93@gmail.com" # In order to search the GenBank database using Entrez, an email is required to ensure people aren't overloading the database with search queries
	for j in list: # for every character in "list" which are the genus+species names
		if i == 1: # We use two different search queries, depending on the group number.
			name=j+"[Orgn] AND ribosomal NOT complete[prop] NOT UNVERIFIED" # For group 1, a name is defined as genus+species name, along with ribosomal. This will search for all results containing ribosomal fasta files of the specified species
		else:
			name=j+"[Orgn] AND mitochondrial NOT complete[prop]" # Same as above but then using mitochondrial information instead of ribosomal. This is done to ensure that all species in each group can be added in the phylogeny
		accsearch = Entrez.esearch(db="nucleotide", term=name, idtype="acc", retmax='1') # Searches GenBank using Entrez.esearch using the searchterm that was defined above. Type=acc gives the results as accessions which will be used later to obtain the fasta information. Retmax=1 gives a maximum result of 1 to remove duplicates in the tree.
		accrecord = Entrez.read(accsearch) # Stores the information from the search in a statement
		accessions = accrecord["IdList"] # IdList returns all the accessions that were found (in this case only one is stored because of the retmax=1
		for acc in accessions: # This allows for multiple accessions to be used if that is desired
			seq=Entrez.efetch(db="nucleotide", id=acc, rettype="fasta", retmode="text") # Entrez.efetch obtains information using the accessions as id. Rettype is set to fasta to obtain the fasta sequences needed to create the phylogenies.
			OutFile.write(seq.read()) # Stores the obtained fasta details in a new file.
	OutFile.close() # Closes the file that was used to store the fasta details
	FileNamex = input+str(i)+".fasta" # Redundent statement but used for our own clarity
	FastaFile = open(FileNamex,'r') # Opens the file which has the fasta information
	FastaContent = FastaFile.read() # Stores the information from the fasta file
	SearchStr = r">\w+\.\d\s(\w\w)\w+\s(\w+).+" # A regular expression statement which searches for the header
	ReplaceStr = r">\1_\2" # A replace string which only selects the genus+species names. The first two letters of the genus are used since our testfiles used two different genera which start with the same letter (Aquilegia, Aconitum)
	FastaContent = re.sub(SearchStr, ReplaceStr, FastaContent, count=0) # Replaces the searchstring with the replacestring. Count = 0 selects all matches instead of only the first one.
	FastaContent = re.sub(r'([ATCG]+)\n([ATCG])', r'\1\2', FastaContent, count=0) # This places all sequences on one line
	FastaContent = re.sub(r"\n\n", r'\n', FastaContent, count=0) # This replaces the double line endings between species with only one line ending
	FastaFile.close() # Closes the opened files
	FasReformat = open("out_"+input+str(i)+".fasta", 'w') # Creates a new file using 'w' for write
	FasReformat.write(FastaContent) # Adds the replaced information in the new file
	FasReformat.close() # Closes the opened file
	os.system("clustalw -INFILE=out_"+FileNamex+" -TYPE=DNA -OUTFILE=Output_phyllip"+str(i)+".phy -OUTPUT=PHYLLIP") # Runs clustalw in bash on the reformatted fasta file and creates a PHYLLIP file as an output.
	print "Completed group "+str(i)+" conversion" # Prints a status report after obtaining the fasta file from each group from the GenBank database
	print "Search term used: ", name # Prints the search term that was used to find the accessions.
	print # Empty line for clarity
	os.system("rm "+input+str(i)+".fasta") # Removing intermediary files that are no longer needed
	os.system("rm tempformat"+str(i)+".txt")
	os.system("rm out_"+input+str(i)+".fasta")
	os.system("rm out_"+input+str(i)+".dnd")

for i in groups: # Not added within the previous "for" statement to run each programme back to back to easier locate errors
	os.system("phyml -i Output_phyllip"+str(i)+".phy -d nt -n 1 -m HKY85") # Uses phyml in bash to create a tree structure which can be used in R to create phylogenetic trees. This uses the newly created PHYLLIP files from each group

for i in groups:
	os.system('tail -n +2 '+input+' | cut -f 1,2,3,5- -d "," | sort -n -k 1 -t "," | grep ^'+str(i)+' | cut -f 2- -d "," > tempchar'+str(i)) # Creates an intermediary file containing the species names with their character values
	os.system('cut -f 3- -d "," tempchar'+str(i)+' > tempcalc'+str(i)) # Creates a file which only includes the character values
	calc=open("tempcalc"+str(i), 'r') # Opens the file with all the character values
	calcu=calc.read() # Stores the information in the file
	calcusplit=calcu.split("\n") # Separates the characters based on line endings so every string contains the values for one species
	del calcusplit[len(calcusplit)-1] # Removes the empty string at the end
	x=[] # Creates an empty list
	for z in calcusplit: # Selects the grouped character values of each species
		num=z
		nums=num.split(',') # Splits the character values
		count=0 # Creates a count statement and sets it to 0
		for j in nums: # Selects each individual character value
			count=count+float(j) # Adds this character value to count
		count = count/len(nums) # Calculates the mean of te character trait
		x.append(count) # Adds the mean to the empty x list
	os.system('tail -n +2 '+input+' | cut -f 1,2,3,5- -d "," | sort -n -k 1 -t "," | grep ^'+str(i)+' | cut -f 2- -d "," | cut -f 1,2 -d "," | tr "," " " > tempnames'+str(i)) # Creates a file containing the names of the species
	names=open("tempnames"+str(i), 'r') # Opens the file with the names
	name=names.read() # stores the names in a statement
	namesplit=name.split("\n") # Splits the names based on line endings
	del namesplit[len(namesplit)-1] # Removes the empty string at the end
	c=[] # Creates an empty list
	for f, b in zip(namesplit, x): # This cycles through the same character number for two statements, so it first selects the first character in namesplit and saves it into f and then stores the first character in x and stores it into b
		c.append(f+": %.2f" % (b)) # Adds the name along with the mean of the character value in the empty c list
	ope=open("fullnames"+str(i), 'a') # Creates a new file for the names and characters
	for h in c:
		ope.write(h+"\n") # Adds the names with characters into a file, separated by line endings
	ope.close() # Closes the file

	os.system("rm Output_phyllip"+str(i)+".phy") # Removes intermediary files which are no longer necessary
	os.system("rm Output_phyllip"+str(i)+".phy_phyml_stats")
	os.system("rm tempnames"+str(i))
        os.system("rm tempcalc"+str(i))
        os.system("rm tempchar"+str(i))




print "Sequencing completed" # Prints when the script is done with all its components



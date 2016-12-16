#!/bin/bash

###
### FROM
### https://github.com/leviaking/gigaword_SLMtoolkit/blob/master/gigaword_compile.sh
###
###
### 2013/09/24. This script is for iterating through the Gigaword corpus folders, gunzip all the .gz files (extract the text files; each .gz contains only one text file, but the text files have no extensions and i'd like them to be .txt).
##
## You'll need to have the corpus files in the original directory structure (the way they are distributed), as described below. If you don't have them set up this way, you should recreate this before running this script.
##gigaword/
##	data/ (directory and files must be present)
##		(NOTE: English Gigaword v3 is divided into "gigaword_eng_3a" and "gigaword_eng_3b"; each contains a folder called "data"; each data folder contains 3 subdirectories, each named "xyz_eng", where xyz is a three letter code representing the data source ("nyt" for New York Times, e.g.). So this script should work on either the "3a" or "3b" data (or both, if run separately or in a shell)
##		xyz_eng/
##			[bunch of .gz files]
##		xyz_eng/
##			[bunch of .gz files]
##		xyz_eng/
##			[bunch of .gz files]
##	textfiles/ (this script will create this directory and the files in it)
##		[uncompressed .gz text files will be put here]
##	fullgw.txt (script will create this file)
##		(this will be the full gigaword corpus, stored as a single text file; it will be huge-- several GB-- so do not try to open it with an editor!)
#
mkdir textfiles
cd data
##this next line finds all the subdirectories of gigaword/data/ (only one level down, I think); enters them one by one; in each subdirectory, it finds every *.gz file and unzips it into the gigaword/textfiles/ directory; so after this line, we have all the text files uncompressed and in one directory
for d in $(for a in $(ls -d -- */); do echo $a; done); do (cd `echo $d`; for f in $(ls *.gz); do gunzip -c $f > ../../textfiles/`echo $(echo $f | sed s-./--) | sed s-.gz-.txt-`; done; cd ..); done 
cd ../textfiles
##this line appends the contents of each text file into a single file: gigaword/gigaword.txt. Note that it strips out any non-ascii characters as it does this. (there are a few funky characters throughout gigaword, and leaving them in causes problems for some programs you may want to train on this data.)
cat *.txt | tr -cd '\11\12\15\40-\176' >> ../gigaword.txt
##note that at this point we essentially have the data in 3 places-- the original .gz files (gigaword/data/*_eng/*.gz), the uncompressed .txt files (gigaword/textfiles/*.txt), and the final gigaword/gigaword.txt file, so we may want to remove the uncompiled .gz and .txt files. The remaining lines would accomplish this; uncomment them if you want to delete the extra data to free up disk space.
cd ..
#rm -r data
rm -r textfiles


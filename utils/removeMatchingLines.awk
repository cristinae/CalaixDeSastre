#!/bin/awk -f

#https://stackoverflow.com/questions/18204904/fast-way-of-finding-lines-in-one-file-that-are-not-in-another

# output lines in file1 that are not in file2
BEGIN { FS="" }                        # preserve whitespace 
(NR==FNR) { ll1[FNR]=$0; nl1=FNR; }    # file1, index by lineno 
(NR!=FNR) { ss2[$0]++; }               # file2, index by string 
END {
    for (ll=1; ll<=nl1; ll++) if (!(ll1[ll] in ss2)) print ll1[ll]
}

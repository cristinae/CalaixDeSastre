#!/usr/bin/perl

###############################################################################
# ACHTUNG! Not working for consecutive lines
# Purpose: Inserting black lines into a file. The position to insert the blanks
#          is listed in a text file
# Author:  Cristina
# Date:    20/02/2019 
###############################################################################

use strict;
use warnings;

#binmode(STDIN, ":utf8");
#binmode(STDOUT, ":utf8");


# Command line arguments
my $num_args = $#ARGV + 1;
if ($num_args != 2) {
    print "\nUsage: $0 <listLinesFile> <fullFile>  >  outputFile \n";
    exit;
}

my $lines2insert=$ARGV[0];
my $completeFile=$ARGV[1];


# Load positions
open LINES, "< $lines2insert" or die "could not open $lines2insert\n";
my $keyRef;
while (<LINES>) {
   chomp;
   $keyRef->{$_} = 1;
}
close LINES;

# Traverse input file and extract selected lines
open FILE2, "< $completeFile" or die "could not open $completeFile\n";
my $i=1;
while (<FILE2>) {
    chomp;
    print STDOUT "$_\n";
    if (defined $keyRef->{$i}) {
        print STDOUT "\n";
    }
    $i++;
}
close FILE2;

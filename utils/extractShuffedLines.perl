#!/usr/bin/perl

###############################################################################
# Purpose: Extracting a subset of lines from a file. The lines to extract are
#          listed in a text file
# Author:  Cristina
# Date:    20/08/2017 
###############################################################################

use strict;
use warnings;

#binmode(STDIN, ":utf8");
#binmode(STDOUT, ":utf8");


# Command line arguments
my $num_args = $#ARGV + 1;
if ($num_args != 2) {
    print "\nUsage: $0 <listLinesFile> <fullFile>  >  extractedLines \n";
    exit;
}

my $lines2extract=$ARGV[0];
my $completeFile=$ARGV[1];

# Load input file
open FILE2, "< $completeFile" or die "could not open $completeFile\n";
my $i=1;
my @sentences;
while (<FILE2>) {
    chomp;
    $sentences[$i]=$_;
    $i++;
}
close FILE2;

# Read lines to extract and extract them
open LINES, "< $lines2extract" or die "could not open $lines2extract\n";
while (<LINES>) {
   chomp; 
    print STDOUT "$sentences[$_]\n";
}
close LINES;



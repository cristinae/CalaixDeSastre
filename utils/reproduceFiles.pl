#!/usr/bin/perl

###############################################################################
# Purpose: Creating a new file B for every line in file A repeted length(fileA)
# Author:  Cristina
# Date:    05/09/2017 
###############################################################################

use strict;
use warnings;

#binmode(STDIN, ":utf8");
#binmode(STDOUT, ":utf8");


# Command line arguments
my $num_args = $#ARGV + 1;
if ($num_args != 1) {
    print "\nUsage: $0 <inputFile> \n";
    exit;
}

my $lines2extract=$ARGV[0];

# Load lines to extract
open LINES, "< $lines2extract" or die "could not open $lines2extract\n";
my $length = 343;
my $i=1;
while (<LINES>) {
   chomp;
   my $sentenceFile = $lines2extract.".s".$i;
   open FILE2, "> $sentenceFile" or die "could not open $sentenceFile\n";
   foreach my $j (1..$length) {
       print FILE2 "$_\n";
   }
   close FILE2;   
   $i++;
}
close LINES;



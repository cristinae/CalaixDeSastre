#!/usr/bin/perl

# ####################################33
# Modificat de
#   http://www.mortis.org.uk/?p=142
# ####################################33


use strict;
use Getopt::Long;


# -- read options ------------------------------------------------------------------
my $opt_t;
my $opt_s;
my $help;
GetOptions ( "t=s" => \$opt_t, "time" => \$opt_t , 
	     "s=s" => \$opt_s, "strech" => \$opt_s , 
	     "help!" => \$help 
           );

if ($help) { usage(); }

# -- check number of argments ------------------------------------------------------
my $NARG = 1;
my $ARGLEN = scalar(@ARGV);
if ($ARGLEN < $NARG) { die usage(); }
my $srt = shift(@ARGV);


# -- open files --------------------------------------------------------------------
open(IN, "< $srt") or die("No s'ha pogut obrir $srt. Error: $!");
open(OUT, "> $srt.tmp") or die("No s'ha pogut crear $srt.tmp. Error: $!");


# -- shifta ------------------------------------------------------------------------
my %scales =  ( 'h' => 3600000,
                'm' => 60000,
                's' => 1000,
                'u' => 0        );
my $strech=1;
if ($opt_s) {
   $strech = $opt_s;
} 

if ($opt_t) {
  my $sign  = substr($opt_t,0,1);
  my $scale = substr($opt_t,length($opt_t)-1, 1);
  my $time  = int(substr($opt_t,1,length($opt_t)-2));

  if ( $sign !~ /[+-]/ || $scale !~ /[hmsu]/ )  {
    die "Time should be [+-]";
  }

  if ( $scales{$scale} )  {
    $time = $time * $scales{$scale};
  }

  if ( $sign =~ /-/ )  {
    $time *= -1;
  }

  while (<IN>)  {
    # 00:01:09,040 --> 00:01:11,713
    if ( /(\d\d):(\d\d):(\d\d),(\d+)\s+-->\s+(\d\d):(\d\d):(\d\d),(\d+)/ )    {
      my ($sh,$sm,$ss,$su,$eh,$em,$es,$eu) = ($1,$2,$3,$4,$5,$6,$7,$8,$9);

      my $s = ($su + ($ss * $scales{'s'}) + ($sm * $scales{'m'}) + ($sh * $scales{'h'}))*$strech + $time;
      my $e = ($eu + ($es * $scales{'s'}) + ($em * $scales{'m'}) + ($eh * $scales{'h'}))*$strech + $time;

      my $rt = 0;
      $sh = int($s/$scales{'h'});
      $rt += ($sh * $scales{'h'});

      $sm = int(($s - $rt) / $scales{'m'});
      $rt += ($sm * $scales{'m'});

      $ss = int(($s - $rt) / $scales{'s'});
      $rt += ($ss * $scales{'s'});

      $su = ($s - $rt);

      $rt = 0;
      $eh = int($e/$scales{'h'});
      $rt += ($eh * $scales{'h'});

      $em = int(($e - $rt) / $scales{'m'});
      $rt += ($em * $scales{'m'});

      $es = int(($e - $rt) / $scales{'s'});
      $rt += ($es * $scales{'s'});

      $eu = ($e - $rt);

      printf OUT "%02d:%02d:%02d,%03d --> %02d:%02d:%02d,%03d\n", $sh,$sm,$ss,$su,$eh,$em,$es,$eu;
    }
    else {
      print OUT $_;
    }
  }
} else{
  print "You need to specify time offset\n";
}

close (IN);
close (OUT);
system ("mv $srt.tmp $srt");


sub usage
{
   $0 =~ /\/([^\/]*$)/;
   print STDERR "\nUsage: ", $0, "  [options]  <file.srt>\n\n";
   print STDERR "Options:\n\n";
   print STDERR "  -t                     : time shift\n";
   print STDERR "  -s                     : strech factor (25/24=1.04)
\n";
   print STDERR "  -help                  : this help\n";
   print STDERR "\nExample: $0 -t +10s AHS.S01E01.Pilot.srt\n\n";
   exit;
}


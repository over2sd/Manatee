#!/usr/bin/perl
require 5.10.1;

use strict;
use warnings;

use Manatee;
use ManateeSQL;
use Manadmin;

my $dbh = &ManateeSQL::getDB();
my %config = (
	'site' => 'Manatee',
);
my %var;

sub dumpBase{
	open FILE, ">", "ccowback.msq" or die $!;
	print FILE "CREATE DATABASE ccow;
USE ccow;
";

	my @result = &ManateeSQL::doQuery(5,$dbh,qq(SHOW TABLES LIKE 'categories_%';));
	foreach my $column (@result) {
		foreach my $row (@{$column}) {;
			&Manadmin::dumpTable($dbh,"$row->[0]",*FILE);
		}
	}
	print FILE "\n";
	&Manadmin::dumpTable($dbh,"cats",*FILE);
	print FILE "\n";
	close FILE;
}

dumpBase();
1;
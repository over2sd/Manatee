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

print "CREATE DATABASE ccow;
USE ccow;
CREATE TABLE cats ( cid INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT, ccode CHAR(4) default NULL, ctext VARCHAR(65) );
";


&Manadmin::dumpBase($dbh,"categories_en","tmp.txt");
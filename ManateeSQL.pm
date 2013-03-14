package ManateeSQL;

require Manatee;
require Exporter;
@ISA = qw(Exporter);
@EXPORT = qw(getDB glot);

sub getDB {
	my $host = 'localhost';
	my $base = 'ccow';
	my $password = '';
	my $username = 'www-data';
	use DBI;
	my $dbh;
	# connect to the database
	$dbh = DBI->connect("DBI:mysql:$base:$host",$username, $password) ||
		die qq{DBI error from connect: "$DBI::errstr"};
	return $dbh;
}

sub doQuery {
	my ($qtype,$dbh,$statement) = @_;
	my $realq;
	if($qtype == 0){
		$realq = $dbh->selectrow_arrayref($statement, { Slice => {} });
	} elsif ($qtype == 1){
		$realq = $dbh->selectall_arrayref($statement, { Slice => {} });
	} else {
		print "Invalid query type";
	}
	return $realq;
}

sub table_exists {
	my ($dbh,$table) = @_;
	my $result = doQuery(0,$dbh,qq(SHOW TABLES LIKE '$table';));
	return (length(@{$result}) == 0) ? 0 : 1;
}

sub glot {
	my ($code,$sql,$lang) = @_;
	my $stage = defined $_[3] ? $_[3] : 5;
	my $out = "";
	my $table = "categories_$lang";
#	print "Seeking categories_$lang...";
	if (table_exists($sql,$table)) {
		$code =~ s/x/o/g;
		$code =~ s/X/o/g;
		my $cmd = qq(SELECT ctext FROM $table WHERE ccode = '$code' LIMIT 1;);
		print "?? $cmd ";
		$result = doQuery(0,$sql,$cmd);
#		print @{$result}[0];
		if ($result) {
			$out = &Manatee::unSQL(@{$result}[0]);
		} else {
			my @aspect = ("Hol","Ras","Dua","Chi","Ter","Fum","Sek","Zab","Med","Neu","Uay","Arz","Pax","Ord","Iyu","Ech");
			my $hx = substr($code,($stage - 1),1);
			$out = "[Unassigned] ($aspect[hex($hx)])";
		}
	} elsif ($lang != "en") {
		print "Fallback to English";
		$out = glot($code,$sql,"en",$stage);
	} else {
		print "Language not found! Fallback failed!";
	}
}

sub glotCrumbs {
	# returns an array loaded with one or more arrays containing the strings needed to print a trail of breadcrumbs in the approrpiate language.
	my @crumbs;
	my ($sql,$code,$stage,$lang) = @_;
	my $a; my $b; my $c;
	if ($stage > 4) {
		print "<!-- Stage reset MS:74 -->";
		$stage = 4;
	}
	if ($stage eq '0' or (substr($code,0,1) eq 'x')) { # already at top
		$a = '5';
		$b = "";
		$c = "Change Languages";
		push(@crumbs,($a,$b,$c));
	} else {
		$a = '6';
		$b = "?lang=$lang";
		$c = "Top (start over)";
		push(@crumbs,($a,$b,$c));
		my $ic = 1;
		while ($ic < $stage and (substr($code,$ic,1) ne 'x')) {
			$a = 6+$ic;
			$snip = substr($code,0,$ic);
			$b = "?lang=$lang&cowc=$snip";
			while (length($snip) < 4) { $snip = $snip . 'o'; }
			$c = glot($snip,$sql,$lang,$ic);
			my @tmp = ($a,$b,$c);
			push(@crumbs,@tmp);
			$ic++;
		}
	}
	print "@crumbs";
	return \@crumbs;
}

1;
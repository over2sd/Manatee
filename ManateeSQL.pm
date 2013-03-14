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
#	print "Seeking categories_$lang...";
	if (table_exists($sql,"categories_$lang")) {
		$code =~ s/x/o/g;
		$code =~ s/X/o/g;
		my $cmd = qq(SELECT ctext FROM categories_$lang WHERE ccode = '$code' LIMIT 1;);
		$result = doQuery(0,$sql,$cmd);
#		print @{$result}[0];
		if ($result) {
			$out = &Manatee::unSQL(@{$result}[0]);
		} else {
			my @aspect = ("Hol","Ras","Dua","Chi","Ter","Fum","Sek","Zab","Med","Neu","Uay","Arz","Pax","Ord","Iyu","Ech");
			$hx = substr($code,($stage - 1),1);
			;
			$out = "[Unassigned] ($aspect[hex($hx)])";
		}
	} elsif ($lang != "en") {
		print "Fallback to English";
		$out = glot($code,$sql,"en",$stage);
	} else {
		print "Language not found! Fallback failed!";
	}
}

1;
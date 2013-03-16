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
#		print "?? $cmd ";
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
	my ($sql,$code,$stage,$lang,$style) = @_;
	$style = (length($style)) ? "&$style" : "";
	my $a; my $b; my $c;
	my $ic = 0;
	if ($stage > 4) {
		print "!-- Stage reset MS:74 --"; # TODO: make a comment after debugging done
		$stage = 4;
	}
	if ($stage eq '0' or (substr($code,0,1) eq 'x')) { # already at top
		$a = '5';
		$style = (length($style)) ? substr($style,0,1,'?') : '';
		$b = "$style";
		$c = "Change Languages";
		push(@{$crumbs[$ic]},($a,$b,$c));
	} else {
		$a = '6';
		$b = "?lang=$lang$style";
		$c = "Top (start over)";
		push(@{$crumbs[$ic]},($a,$b,$c));
		$ic++;
		while ($ic < $stage and (substr($code,$ic,1) ne 'x')) {
			$a = 6+$ic;
			$snip = substr($code,0,$ic);
			$b = "?lang=$lang$style&cowc=$snip";
			while (length($snip) < 4) { $snip = $snip . 'o'; }
			$c = glot($snip,$sql,$lang,$ic);
			my @tmp = ($a,$b,$c);
			push(@{$crumbs[$ic]},@tmp);
			$ic++;
		}
	}
	return @crumbs;
}

sub glotSubs{
	my @subs;
	my ($sql,$code,$stage,$lang) = @_;
	if ($stage == 4) { return @subs; }
	for (my $i = 0; $i < 16; $i++) {
		my $c = sprintf("%x", $i);
		my $scode = substr($code,0,$stage);
		$scode = $scode . $c;
		$scode = &Manatee::cleanCode($scode);
		my $sdesc = glot($scode,$sql,$lang,$stage + 1);
		my @subarr = ($scode,$c,$sdesc);
		push(@{$subs[$i]},@subarr);
	}
	return @subs;
}

1;
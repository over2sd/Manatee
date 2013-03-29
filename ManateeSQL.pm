package ManateeSQL;

require Manatee;
require Exporter;
@ISA = qw(Exporter);
@EXPORT = qw(getDB glot);

sub getDB {
#	my ($a,$b,$c,$d) = @_
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
	} elsif ($qtype == 2) {
		$realq = $dbh->do($statement) or $realq = $dbh->errstr;
		if($realq =~ m/^[0-9]+$/) {
			return $realq; 
		} else {
			return $dbh->errstr;
		}
	} elsif ($qtype == 3){
		$realq = $dbh->selectall_hashref($statement, { Slice => {} });
	} elsif ($qtype == 5){
		$realq = $dbh->selectall_arrayref($statement);
	} elsif ($qtype == 6){
		$realq = $dbh->selectrow_array($statement);
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
	return $out;
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
		$style = (length($style)) ? substr($style,0,1,'?') : '?lang=';
		$b = "$style";
		$c = "Change Languages??";
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
#		print "<br />$scode,$sql,$lang,$stage";
		my $sdesc = glot($scode,$sql,$lang,$stage + 1);
		my @subarr = ($scode,$c,$sdesc);
		push(@{$subs[$i]},@subarr);
	}
	return @subs;
}

sub glotSuggs{
	my @suggs;
	my ($sql,$code,$lang) = @_;
	$code =~ s/x/o/g;
	$code =~ s/X/o/g;
#	$code = &Manatee::cleanCode($code);
	$cmd = qq(SELECT ctext,rationale FROM cats WHERE ccode = '$code' AND lang = '$lang';);
	$result = doQuery(5,$sql,$cmd);
	return @$result;
}

sub countRecords{
	my ($dbh,$type,$table,$code,$lang,$ip) = @_;
	my $cri;
	if ($type == 0 && length($ip) > 6 && length($code) == 4) {
		$cri = qq(ccode = '$code' AND lang = '$lang' AND ip = '$ip' AND TIMESTAMPADD(DAY,7,time) > NOW());
	} elsif ($type == 1) {
		$cri = qq(ccode = '$code' AND lang = '$lang');
	} else {
		$cri = "0";
	}
	my $cmd = qq(SELECT COUNT(*) as c FROM $table WHERE $cri;);
	my $count = doQuery(5,$dbh,$cmd);
	my $out;
	foreach my $x (@{$count}) {
		$out = "$x->[0]";
	}
	return $out;
}

sub pushSugg{
	my ($dbh,$ip,$code,$desc,$rat,$lang) = @_;
	$code =~ s/x/o/g;
	$code =~ s/X/o/g;
	my $toosoon = countRecords($dbh,0,"cats",$code,$lang,$ip);
	if ($toosoon) {
		return 1; # too soon
	} elsif ($desc =~ m/;/) { return 2;
	} elsif ($desc =~ m/\[/) { return 2;
	} elsif ($desc =~ m/\]/) { return 2;
	} elsif ($rat =~ m/;/) { return 2;
	} elsif ($rat =~ m/\[/) { return 2;
	} elsif ($rat =~ m/\]/) { return 2;
	} elsif (length($rat) < 20) { return 2;
	} elsif (length($desc) < 5) { return 2;
	} else {
		my $cmd = qq(INSERT INTO cats (ccode,ctext,rationale,ip,lang,time) VALUES ('$code','$desc','$rat','$ip','$lang',NOW()););
		my $success = doQuery(2,$dbh,$cmd);
		if($success == 1) { #yay!
#			print "Query successful";
			return 0;
		} elsif($success =~ m/^[0-9]+$/) { # wrong number of rows?
#			print "Row count error: $success"
			return 3;
		} else { # not an expected numeric return value
#			print "Database Error: $success. Please contact the DBA!";
			return -1;
		}
	}
}

1;
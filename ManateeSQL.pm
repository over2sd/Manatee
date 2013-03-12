package ManateeSQL;

require Exporter;
@ISA = qw(Exporter);
@EXPORT = qw(getDB);

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

1;